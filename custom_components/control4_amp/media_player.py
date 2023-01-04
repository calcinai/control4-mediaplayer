""" Control4-mediaplayer """
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers import ConfigType
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import DiscoveryInfoType

from .control4_amp import Control4AmpChannel, Control4Amp

import logging
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from homeassistant.components.media_player import (
    ENTITY_ID_FORMAT,
    PLATFORM_SCHEMA,
    MediaPlayerEntity
)

from homeassistant.components.media_player.const import (
    MediaPlayerEntityFeature
)

from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_FRIENDLY_NAME,
    CONF_NAME,
    STATE_OFF,
    STATE_ON,
)

from . import DOMAIN as CONTROL4_DOMAIN

_LOGGER = logging.getLogger(__name__)

#Why is this needed? Does it initialize variables?
CONF_ON_VOLUME = "on_volume"
CONF_CHANNEL = "channel"
DEFAULT_VOLUME = 5

SUPPORT_CONTROL4 = (
    MediaPlayerEntityFeature.VOLUME_SET |
    MediaPlayerEntityFeature.VOLUME_STEP |
    MediaPlayerEntityFeature.TURN_ON |
    MediaPlayerEntityFeature.TURN_OFF |
    MediaPlayerEntityFeature.SELECT_SOURCE
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Optional(CONF_ON_VOLUME, default=DEFAULT_VOLUME): cv.positive_int,
        vol.Required(CONF_CHANNEL): cv.positive_int,
    }
)

async def async_setup_platform(
        hass: HomeAssistant,
        config: ConfigType,
        add_entities: AddEntitiesCallback,
        discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Control4Amp binary sensor platform."""
    sensors = []
    for name, c4_amp in hass.data[CONTROL4_DOMAIN].items():

        sensors.append(Control4MediaPlayer(config.get(CONF_NAME), c4_amp))
    add_entities(sensors)


class Control4MediaPlayer(MediaPlayerEntity):
    #Research at https://developers.home-assistant.io/docs/core/entity/media-player/

    def __init__(self, name, channel:Control4AmpChannel):
        #self.hass = hass
        self._domain = __name__.split(".")[-2]
        self._name = name
        self._ampChannel = channel
        self._source = 1
        self._source_list = ['1','2','3','4']
        self._on_volume = on_volume / 100
        self._state = STATE_OFF
        self._available = True
        
        self._ampChannel = control4AmpChannel(host, port, channel)

    async def async_update(self):
        # Not sure if update(self) is required.
        _LOGGER.warning("update...")
       
    @property
    def should_poll(self):
        return False

    @property
    def icon(self) -> str | None:
        """Return the icon."""
        return "mdi:speaker"

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def source(self):
        return self._source

    @property
    def source_list(self):
        return self._source_list

    @property
    def volume_level(self):
        """Volume level of the media player (0..1)."""
        return self._ampChannel.volume 

    @property
    def supported_features(self):
        """Flag media player features that are supported."""
        return SUPPORT_CONTROL4

    async def async_select_source(self,source):
        self._source = source
        self._ampChannel.source = source
        self.schedule_update_ha_state()
        _LOGGER.warning("Source set to " + str(self._ampChannel.source))

    async def async_turn_on(self):
        _LOGGER.warning("Turning on...")
        self._ampChannel.volume = self._on_volume
        result = self._ampChannel.turn_on()
        self._state = STATE_ON
        self.schedule_update_ha_state()

    async def async_turn_off(self):
        _LOGGER.warning("Turning off...")
        self._ampChannel.volume = self._on_volume
        result = self._ampChannel.turn_off()
        self._state = STATE_OFF 
        self.schedule_update_ha_state()
       
    async def async_volume_up(self):
        self._ampChannel.volume = self._ampChannel.volume + .01
        self.schedule_update_ha_state()
        _LOGGER.warning("volume set to " + str(self._ampChannel.volume))

    async def async_volume_down(self):
        self._ampChannel.volume = self._ampChannel.volume - .01
        self.schedule_update_ha_state()
        _LOGGER.warning("volume set to " + str(self._ampChannel.volume))

    async def async_set_volume_level(self, volume):
        self._ampChannel.volume  = volume 
        self.schedule_update_ha_state()
        _LOGGER.warning("volume set to " + str(self._ampChannel.volume))
