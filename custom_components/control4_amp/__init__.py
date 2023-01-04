"""Support for Control4 Amps."""
import logging
import voluptuous as vol

from homeassistant.const import (
    ATTR_ID,
    ATTR_NAME,
    CONF_NAME,
    CONF_HOST,
    CONF_PORT,
    CONF_TIMEOUT,
    Platform,
)
from homeassistant.core import HomeAssistant, ServiceCall
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers.typing import ConfigType

from .control4_amp import Control4Amp, Control4AmpInput

_LOGGER = logging.getLogger(__name__)

DOMAIN = "control4_amp"
CONF_INPUTS = "inputs"
CONF_OUTPUTS = "outputs"
CONF_DIGITAL = "digital"


DEFAULT_PORT = 8750
DEFAULT_TIMEOUT = 2

INPUT_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Optional(CONF_DIGITAL, default=False): cv.boolean,
    }
)

HOST_CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.positive_int,
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.positive_int,
    }
)

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: {vol.unicode: HOST_CONFIG_SCHEMA}}, extra=vol.ALLOW_EXTRA
)


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Control4 Amp component."""

    hass.data[DOMAIN] = {}
    success = True

    for name, conf in config[DOMAIN].items():
        c4_amp = Control4Amp(
            conf.get(CONF_HOST),
            conf.get(CONF_PORT),
            conf.get(CONF_TIMEOUT),
        )
        hass.data[DOMAIN][name] = c4_amp

        for channel, channel_conf in conf.get('inputs'):
            channel = Control4AmpInput(c4_amp)

    hass.async_create_task(
        async_load_platform(hass, Platform.BINARY_SENSOR, DOMAIN, {}, config)
    )

    return success
