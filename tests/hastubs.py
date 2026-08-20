"""Test scaffolding: load component modules without a Home Assistant install.

The suite tests the integration's pure logic (store, matching, migration,
codes, AI parsing). The component modules only touch a handful of Home
Assistant symbols at import time, so tiny stubs stand in for those and the
modules are loaded straight from their files — the package ``__init__``
(which pulls in the full frontend/panel machinery) never runs.
"""

from __future__ import annotations

import importlib.util
import sys
import types
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

COMPONENT_DIR = (
    Path(__file__).resolve().parents[1] / "custom_components" / "fridge_assistant"
)
_PKG = "fa_under_test"


def _register(name: str) -> types.ModuleType:
    mod = types.ModuleType(name)
    sys.modules[name] = mod
    return mod


def install_stubs() -> None:
    """Install minimal ``homeassistant`` stand-ins (idempotent)."""
    if "homeassistant" in sys.modules:
        return

    ha = _register("homeassistant")

    core = _register("homeassistant.core")

    class HomeAssistant:  # noqa: D401 - only used as a type at runtime
        """Type stand-in."""

    core.HomeAssistant = HomeAssistant

    helpers = _register("homeassistant.helpers")

    storage = _register("homeassistant.helpers.storage")

    class Store:
        """Records saves; behaves like an empty store on load."""

        def __init__(self, hass, version, key, **kwargs):
            self.hass = hass
            self.version = version
            self.key = key
            self.saved = None

        async def async_load(self):
            return None

        async def async_save(self, data):
            self.saved = data

    storage.Store = Store

    aiohttp_client = _register("homeassistant.helpers.aiohttp_client")
    aiohttp_client.async_get_clientsession = lambda hass: None

    util = _register("homeassistant.util")
    dt = _register("homeassistant.util.dt")
    dt.now = lambda: datetime.now(timezone.utc)
    dt.utc_from_timestamp = lambda ts: datetime.fromtimestamp(ts, timezone.utc)
    util.dt = dt

    components = _register("homeassistant.components")
    persistent_notification = _register("homeassistant.components.persistent_notification")
    components.persistent_notification = persistent_notification

    config_entries = _register("homeassistant.config_entries")
    config_entries.ConfigEntry = type("ConfigEntry", (), {})
    ha.config_entries = config_entries

    dispatcher = _register("homeassistant.helpers.dispatcher")
    dispatcher.async_dispatcher_send = lambda *a, **k: None
    helpers.dispatcher = dispatcher

    ha.core = core
    ha.helpers = helpers
    ha.util = util
    ha.components = components
    helpers.storage = storage
    helpers.aiohttp_client = aiohttp_client


def load_module(name: str) -> types.ModuleType:
    """Load ``custom_components/fridge_assistant/<name>.py`` for testing.

    Modules are loaded under a synthetic package so their relative imports
    (``from .const import …``) resolve between each other, while the real
    package ``__init__`` stays untouched.
    """
    install_stubs()
    full = f"{_PKG}.{name}"
    if full in sys.modules:
        return sys.modules[full]
    if _PKG not in sys.modules:
        pkg = types.ModuleType(_PKG)
        pkg.__path__ = [str(COMPONENT_DIR)]
        sys.modules[_PKG] = pkg
    spec = importlib.util.spec_from_file_location(full, COMPONENT_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[full] = module
    spec.loader.exec_module(module)
    return module


def fake_hass(language: str = "nl") -> SimpleNamespace:
    """The minimal ``hass`` shape the store/const helpers read."""
    return SimpleNamespace(config=SimpleNamespace(language=language))
