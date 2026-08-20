"""Expose Fridge Assistant intents as Assist LLM tools (HA 2024.10+)."""

from __future__ import annotations

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import intent
from homeassistant.helpers.llm import LLM_API_ASSIST, IntentTool, LLMContext

from .intent import INTENT_LIST_INGREDIENTS, INTENT_LIST_INVENTORY

_INTENT_TYPES = frozenset({INTENT_LIST_INGREDIENTS, INTENT_LIST_INVENTORY})


@callback
def async_get_tools(
    hass: HomeAssistant, llm_context: LLMContext, api_id: str
):
    """Return inventory intents for the built-in Assist API."""
    del llm_context  # same tools for every Assist request
    if api_id != LLM_API_ASSIST:
        return None
    tools = [
        IntentTool(handler.intent_type, handler)
        for handler in intent.async_get(hass)
        if handler.intent_type in _INTENT_TYPES
    ]
    if not tools:
        return None
    try:
        from homeassistant.components.llm import LLMTools
    except ImportError:
        return None
    return LLMTools(tools=tools)
