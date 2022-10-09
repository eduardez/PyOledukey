"""
MicroPython PCF8575 16-Bit I2C I/O Expander with Interrupt
https://github.com/mcauser/micropython-pcf8575

MIT License
Copyright (c) 2019 Mike Causer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from adafruit_bus_device.i2c_device import I2CDevice
import digitalio
import time
import busio

try:
    # This is only needed for typing
    import busio  # pylint: disable=unused-import
except ImportError:
    pass



class PCF8575:
    def __init__(self, i2c, address=0x20):
        self.i2c_device = I2CDevice(i2c, address)
        self._port = bytearray(2)
        while not i2c.try_lock():
            pass

        try:
            while True:
                print(
                    "I2C addresses found:",
                    [hex(device_address) for device_address in i2c.scan()],
                )
                time.sleep(2)
                break
        finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
            i2c.unlock()
            
    @property
    def port(self):
        self._read()
        return self._port[0] | (self._port[1] << 8)

    @port.setter
    def port(self, value):
        self._port[0] = value & 0xff
        self._port[1] = (value >> 8) & 0xff
        self._write()

    def pin(self, pin, value=None):
        #print(f'Pin: {pin}, value: {value}')
        #value = True
        pin = self.validate_pin(pin)
        if value is None:
            self._read()
            return (self._port[pin // 8] >> (pin % 8)) & 1
        else:
            if value:
                self._port[pin // 8] |= (1 << (pin % 8))
            else:
                self._port[pin // 8] &= ~(1 << (pin % 8))
            self._write()

    def toggle(self, pin):
        # pin valid range 0..7 and 10-17 (shifted to 8-15)
        pin = self.validate_pin(pin)
        self._port[pin // 8] ^= (1 << (pin % 8))
        self._write()

    def validate_pin(self, pin):
        return pin
        if not 0 <= pin <= 7 and not 10 <= pin <= 17:
            raise ValueError('Invalid pin {}. Use 0-7 or 10-17.'.format(pin))
        if pin >= 10:
            pin -= 2
        return pin

    def _read(self):
        with self.i2c_device as i2c:
            i2c.readinto(self._port)
        
    def _write(self):
        with self.i2c_device as i2c:
            i2c.write(self._port)

    def get_pin(self, pin):
        """Convenience function to create an instance of the DigitalInOut class
        pointing at the specified pin of this PCF8575 device.
        :param int pin: pin to use for digital IO, 0 to 7 and 10 to 17
        """
        assert 0 <= pin <= 15
        return DigitalInOut(pin, self)




"""
`digital_inout`
====================================================
Digital input/output of the PCF8575.
* Author(s): Tony DiCola
"""


class DigitalInOut:
    """Digital input/output of the PCF8575.  The interface is exactly the
    same as the digitalio.DigitalInOut class, however:

      - PCF8575 does not support pull-down resistors
      - PCF8575 does not actually have a sourcing transistor, instead there's
        an internal pullup

    Exceptions will be thrown when attempting to set unsupported pull
    configurations.
    """

    def __init__(self, pin_number, pcf):
        """Specify the pin number of the PCF8575 0..7, and instance."""
        self._pin = pin_number
        self._pcf: PCF8575 = pcf
        self._dir = (
            digitalio.Direction.INPUT
        )  # this is meaningless but we need something!

    # kwargs in switch functions below are _necessary_ for compatibility
    # with DigitalInout class (which allows specifying pull, etc. which
    # is unused by this class).  Do not remove them, instead turn off pylint
    # in this case.
    # pylint: disable=unused-argument
    def switch_to_output(self, value=False, **kwargs):
        """Switch the pin state to a digital output with the provided starting
        value (True/False for high or low, default is False/low).
        """
        self.direction = digitalio.Direction.OUTPUT
        self.value = value
        self._pcf.pin(self._pin, value=value)

    def switch_to_input(self, pull=None, **kwargs):
        """Switch the pin state to a digital input which is the same as
        setting the light pullup on.  Note that true tri-state or
        pull-down resistors are NOT supported!
        """
        self.direction = digitalio.Direction.INPUT
        self.pull = pull
        self._pcf.pin(self._pin)

    # pylint: enable=unused-argument

    @property
    def value(self):
        """The value of the pin, either True for high/pulled-up or False for
        low.
        """
        return self._pcf.pin(self._pin)

    @value.setter
    def value(self, val):
        self._pcf.pin(self._pin, val)

    @property
    def direction(self):
        """
        Setting a pin to OUTPUT drives it low, setting it to
        an INPUT enables the light pullup.
        """
        return self._dir

    @direction.setter
    def direction(self, val):
        if val == digitalio.Direction.INPUT:
            # for inputs, turn on the pullup (write high)
            self._pcf.pin(self._pin, True)
            self._dir = val
        elif val == digitalio.Direction.OUTPUT:
            # for outputs, turn on the transistor (write low)
            self._pcf.pin(self._pin, False)
            self._dir = val
        else:
            raise ValueError("Expected INPUT or OUTPUT direction!")

    @property
    def pull(self):
        """
        Pull-up is always activated so always return the same thing
        """
        return digitalio.Pull.UP

    @pull.setter
    def pull(self, val):
        if val is digitalio.Pull.UP:
            # for inputs, turn on the pullup (write high)
            self._pcf.pin(self._pin, True)
        else:
            self._pcf.pin(self._pin, True)

