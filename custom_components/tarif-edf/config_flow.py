"""Config flow for Tarif EDF integration."""
from __future__ import annotations
import logging
from typing import Any
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.core import callback
from homeassistant.helpers.selector import SelectSelector
from .const import (
    DOMAIN,
    CONTRACT_TYPE_BASE,
    CONTRACT_TYPE_HPHC,
    DEFAULT_BASE_PRICE,
    DEFAULT_HP_PRICE,
    DEFAULT_HC_PRICE,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER = vol.Schema(
    {
        vol.Required("contract_power", default="6"): SelectSelector({
            "options": ['3', '6', '9', '12', '15'],
            "mode": "dropdown"
        }),
        vol.Required("contract_type"): vol.In({
            CONTRACT_TYPE_BASE: 'Base',
            CONTRACT_TYPE_HPHC: 'Heures pleines / Heures creuses',
        }),
        vol.Optional("base_price", default=DEFAULT_BASE_PRICE): float,
        vol.Optional("hp_price", default=DEFAULT_HP_PRICE): float,
        vol.Optional("hc_price", default=DEFAULT_HC_PRICE): float,
    }
)

@config_entries.HANDLERS.register(DOMAIN)
class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Tarif EDF."""
    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", 
                data_schema=STEP_USER
            )

        return self.async_create_entry(
            title="Option "+str.upper(user_input['contract_type']) + ", " + user_input['contract_power']+"kVA",
            data=user_input
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return OptionsFlowHandler(config_entry)

class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        contract_type = self.config_entry.data.get("contract_type")
        options = {}

        if contract_type == CONTRACT_TYPE_BASE:
            options["base_price"] = vol.Optional(
                "base_price", 
                default=self.config_entry.data.get("base_price", DEFAULT_BASE_PRICE)
            )
        elif contract_type == CONTRACT_TYPE_HPHC:
            options.update({
                "hp_price": vol.Optional(
                    "hp_price", 
                    default=self.config_entry.data.get("hp_price", DEFAULT_HP_PRICE)
                ),
                "hc_price": vol.Optional(
                    "hc_price", 
                    default=self.config_entry.data.get("hc_price", DEFAULT_HC_PRICE)
                )
            })

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(options)
        )
