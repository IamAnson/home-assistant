"""
Support for Insteon lights via PowerLinc Modem.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/light.insteon/
"""
import asyncio
import logging

from homeassistant.components.insteon import InsteonEntity
from homeassistant.components.light import (
    ATTR_BRIGHTNESS, SUPPORT_BRIGHTNESS, Light)

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['insteon']

MAX_BRIGHTNESS = 255


@asyncio.coroutine
def async_setup_platform(hass, config, async_add_entities,
                         discovery_info=None):
    """Set up the Insteon component."""
    insteon_modem = hass.data['insteon'].get('modem')

    address = discovery_info['address']
    device = insteon_modem.devices[address]
    state_key = discovery_info['state_key']

    _LOGGER.debug('Adding device %s entity %s to Light platform',
                  device.address.hex, device.states[state_key].name)

    new_entity = InsteonDimmerDevice(device, state_key)

    async_add_entities([new_entity])


class InsteonDimmerDevice(InsteonEntity, Light):
    """A Class for an Insteon device."""

    @property
    def brightness(self):
        """Return the brightness of this light between 0..255."""
        onlevel = self._insteon_device_state.value
        return int(onlevel)

    @property
    def is_on(self):
        """Return the boolean response if the node is on."""
        return bool(self.brightness)

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_BRIGHTNESS

    @asyncio.coroutine
    def async_turn_on(self, **kwargs):
        """Turn device on."""
        if ATTR_BRIGHTNESS in kwargs:
            brightness = int(kwargs[ATTR_BRIGHTNESS])
            self._insteon_device_state.set_level(brightness)
        else:
            self._insteon_device_state.on()

    @asyncio.coroutine
    def async_turn_off(self, **kwargs):
        """Turn device off."""
        self._insteon_device_state.off()
