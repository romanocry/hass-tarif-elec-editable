"""Data update coordinator for the Tarif EDF integration."""
from __future__ import annotations
from datetime import timedelta
from typing import Any
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import TimestampDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

class TarifEdfDataUpdateCoordinator(TimestampDataUpdateCoordinator):
    """Data update coordinator for the Tarif EDF integration."""
    
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass=hass,
            logger=_LOGGER,
            name=entry.title,
            update_interval=timedelta(minutes=60),
        )
        self.config_entry = entry
        self.data = entry.data

    async def _async_update_data(self) -> dict[str, Any]:
        """Get the latest data."""
        return self.config_entry.data
