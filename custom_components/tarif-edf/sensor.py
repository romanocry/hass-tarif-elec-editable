from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.components.sensor import (
    SensorEntity,
)
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from .coordinator import TarifEdfDataUpdateCoordinator
from .const import (
    DOMAIN,
    CONTRACT_TYPE_BASE,
    CONTRACT_TYPE_HPHC,
)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: TarifEdfDataUpdateCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]["coordinator"]
    
    sensors = []
    if coordinator.data['contract_type'] == CONTRACT_TYPE_BASE:
        sensors = [
            TarifEdfSensor(coordinator, 'base_price', 'Tarif Base TTC', unit_of_measurement='EUR/kWh'),
        ]
    elif coordinator.data['contract_type'] == CONTRACT_TYPE_HPHC:
        sensors = [
            TarifEdfSensor(coordinator, 'hc_price', 'Tarif Heures creuses TTC', unit_of_measurement='EUR/kWh'),
            TarifEdfSensor(coordinator, 'hp_price', 'Tarif Heures pleines TTC', unit_of_measurement='EUR/kWh'),
        ]

    async_add_entities(sensors, False)

class TarifEdfSensor(CoordinatorEntity, SensorEntity):
    """Représentation d'un capteur Tarif EDF."""
    
    def __init__(self, coordinator, coordinator_key: str, name: str, unit_of_measurement: str = None) -> None:
        """Initialisation du capteur Tarif EDF."""
        super().__init__(coordinator)
        
        contract_name = str.upper(self.coordinator.data['contract_type']) + " " + self.coordinator.data['contract_power'] + "kVA"
        
        self._coordinator_key = coordinator_key
        self._name = name
        self._attr_unique_id = f"tarif_edf_{self._name}"
        self._attr_name = name
        
        self._attr_device_info = DeviceInfo(
            name=f"Tarif EDF - {contract_name}",
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, f"Tarif EDF - {contract_name}")},
            manufacturer="Tarif EDF",
            model=contract_name,
        )
        
        if unit_of_measurement is not None:
            self._attr_unit_of_measurement = unit_of_measurement

    @property
    def native_value(self):
        """Retourne l'état du capteur."""
        if self._coordinator_key not in self.coordinator.data:
            return 'indisponible'
        return self.coordinator.data[self._coordinator_key]

    @property
    def extra_state_attributes(self):
        """Retourne les attributs d'état."""
        return {
            'updated_at': self.coordinator.last_update_success_time,
            'contract_type': self.coordinator.data['contract_type'],
            'contract_power': self.coordinator.data['contract_power']
        }

    @property
    def available(self) -> bool:
        """Retourne si l'entité est disponible."""
        return self.coordinator.last_update_success and self._coordinator_key in self.coordinator.data
