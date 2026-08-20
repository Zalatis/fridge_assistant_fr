"""Voice and Assist intents for Fridge Assistant inventory."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.core import HomeAssistant
from homeassistant.helpers import intent
from homeassistant.util import dt as dt_util

from .const import DOMAIN, KIND_INGREDIENT, LOCATIONS, resolve_language
from .coordinator import (
    format_inventory_speech,
    get_runtime,
    inventory_item_row,
    sorted_inventory_items,
)

INTENT_LIST_INGREDIENTS = "FridgeAssistantListIngredients"
INTENT_LIST_INVENTORY = "FridgeAssistantListInventory"

_LOCATION_ALIASES = {
    "frigo": "fridge",
    "réfrigérateur": "fridge",
    "refrigerateur": "fridge",
    "koelkast": "fridge",
    "congélateur": "freezer",
    "congelateur": "freezer",
    "vriezer": "freezer",
    "garde-manger": "pantry",
    "buiten koelkast": "pantry",
    "fridge": "fridge",
    "refrigerator": "fridge",
    "freezer": "freezer",
    "pantry": "pantry",
}


def _normalize_location(value: str | None) -> str | None:
    if not value:
        return None
    key = value.strip().lower()
    mapped = _LOCATION_ALIASES.get(key, key)
    return mapped if mapped in LOCATIONS else None


class _FridgeIntentBase(intent.IntentHandler):
    """Shared setup for Assist / voice handlers."""

    platforms = None  # expose as Assist LLM tools

    def _runtime(self, hass: HomeAssistant):
        runtime = get_runtime(hass)
        if runtime is None:
            raise intent.IntentHandleError("Fridge Assistant is not configured.")
        return runtime

    def _rows(self, runtime, today, *, ingredients_only: bool) -> list[dict[str, Any]]:
        items = sorted_inventory_items(runtime.store)
        if ingredients_only:
            items = [i for i in items if i.get("kind") == KIND_INGREDIENT]
        return [inventory_item_row(i, today) for i in items]


class ListIngredientsIntentHandler(_FridgeIntentBase):
    """List individual ingredients (kind=ingredient) in the inventory."""

    intent_type = INTENT_LIST_INGREDIENTS
    description = (
        "List individual ingredients currently stored in the fridge, freezer or pantry. "
        "Returns each name, expiry date, quantity and open portion count."
    )

    async def async_handle(self, intent_obj: intent.Intent) -> intent.IntentResponse:
        runtime = self._runtime(intent_obj.hass)
        lang = resolve_language(intent_obj.hass)
        today = dt_util.now().date()
        rows = self._rows(runtime, today, ingredients_only=True)
        speech = format_inventory_speech(rows, lang, intro_key="ingredients_intro")
        response = intent_obj.create_response()
        response.async_set_speech(speech)
        response.async_set_card("Fridge Assistant", speech)
        return response


class ListInventoryIntentHandler(_FridgeIntentBase):
    """List every active inventory item."""

    intent_type = INTENT_LIST_INVENTORY
    description = (
        "List all food items currently in the fridge inventory, including dishes and "
        "ingredients, with expiry dates, quantities and portions."
    )
    slot_schema = {
        vol.Optional("location"): intent.non_empty_string,
    }

    async def async_handle(self, intent_obj: intent.Intent) -> intent.IntentResponse:
        runtime = self._runtime(intent_obj.hass)
        lang = resolve_language(intent_obj.hass)
        today = dt_util.now().date()
        loc = _normalize_location(intent_obj.slots.get("location", {}).get("value"))
        items = sorted_inventory_items(runtime.store)
        if loc:
            items = [i for i in items if i.get("location") == loc]
        rows = [inventory_item_row(i, today) for i in items]
        speech = format_inventory_speech(rows, lang, intro_key="inventory_intro")
        response = intent_obj.create_response()
        response.async_set_speech(speech)
        response.async_set_card("Fridge Assistant", speech)
        return response


def async_register_intents(hass: HomeAssistant) -> None:
    """Register intent handlers once (shared across config entries)."""
    if hass.data.get(DOMAIN, {}).get("intents_registered"):
        return
    handlers: list[intent.IntentHandler] = [
        ListIngredientsIntentHandler(),
        ListInventoryIntentHandler(),
    ]
    for handler in handlers:
        intent.async_register(hass, handler)
    bucket = hass.data.setdefault(DOMAIN, {})
    bucket["intent_handlers"] = handlers
    bucket["intents_registered"] = True


def async_unregister_intents(hass: HomeAssistant) -> None:
    """Remove intent handlers when the integration is fully unloaded."""
    bucket = hass.data.get(DOMAIN, {})
    if not bucket.get("intents_registered"):
        return
    for handler in bucket.get("intent_handlers", []):
        intent.async_remove(hass, handler)
    bucket.pop("intent_handlers", None)
    bucket["intents_registered"] = False
