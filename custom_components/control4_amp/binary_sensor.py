"""Support for Control4 binary sensors."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .control4_amp import Control4Amp

from . import DOMAIN as CONTROL4_DOMAIN


async def async_setup_platform(
        hass: HomeAssistant,
        config: ConfigType,
        add_entities: AddEntitiesCallback,
        discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Control4Amp binary sensor platform."""
    sensors = []
    for name, c4_amp in hass.data[CONTROL4_DOMAIN].items():
        sensors.append(Control4BinarySensor(name, c4_amp))
    add_entities(sensors)


class Control4BinarySensor(BinarySensorEntity):
    """Representation of the availability of the amp as a binary sensor."""

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_icon = 'mdi:dns'

    def __init__(self, name: str, amp: Control4Amp) -> None:
        """Initialize availability sensor."""
        self._attr_name = name
        self._amp = amp

    def update(self) -> None:
        """Update the state of the sensor (availability of the amp)."""
        self._attr_is_on = self._amp.is_available
