# See docs/encoder.md for how to use

import busio
import digitalio
from supervisor import ticks_ms

from kmk.modules import Module

# NB : not using rotaryio as it requires the pins to be consecutive


class BaseEncoder:

    VELOCITY_MODE = True

    def __init__(self, is_inverted=False, divisor=4):

        self.is_inverted = is_inverted
        self.divisor = divisor

        self._state = None
        self._start_state = None
        self._direction = None
        self._pos = 0
        self._button_state = True
        self._button_held = None
        self._velocity = 0

        self._movement = 0
        self._timestamp = ticks_ms()

        # callback functions on events. Need to be defined externally
        self.on_move_do = None
        self.on_button_do = None

    def get_state(self):
        return {
            'direction': self.is_inverted and -self._direction or self._direction,
            'position': self.is_inverted and -self._pos or self._pos,
            'is_pressed': not self._button_state,
            'velocity': self._velocity,
        }

    def update_state(self):
        # Rotation events
        new_state = (self.pin_a.get_value(), self.pin_b.get_value())
        
        if new_state != self._state:
            # encoder moved
            self._movement += 1
            # false / false and true / true are common half steps
            # looking on the step just before helps determining
            # the direction
            if new_state[0] == new_state[1] and self._state[0] != self._state[1]:
                if new_state[1] == self._state[0]:
                    self._direction = 1
                else:
                    self._direction = -1

            # when the encoder settles on a position (every 2 steps)
            if new_state[0] == new_state[1]:
                # an encoder returned to the previous
                # position halfway, cancel rotation
                if (
                    self._start_state[0] == new_state[0]
                    and self._start_state[1] == new_state[1]
                    and self._movement <= 2
                ):
                    self._movement = 0
                    self._direction = 0

                # when the encoder made a full loop according to its divisor
                elif self._movement >= self.divisor - 1:
                    # 1 full step is 4 movements (2 for high-resolution encoder),
                    # however, when rotated quickly, some steps may be missed.
                    # This makes it behave more naturally
                    real_movement = self._movement // self.divisor
                    self._pos += self._direction * real_movement
                    if self.on_move_do is not None:
                        for i in range(real_movement):
                            self.on_move_do(self.get_state())

                    # Rotation finished, reset to identify new movement
                    self._movement = 0
                    self._direction = 0
                    self._start_state = new_state

            self._state = new_state

        # Velocity
        self.velocity_event()

        # Button event
        self.button_event()

    def velocity_event(self):
        if self.VELOCITY_MODE:
            new_timestamp = ticks_ms()
            self._velocity = new_timestamp - self._timestamp
            self._timestamp = new_timestamp

    def button_event(self):
        raise NotImplementedError('subclasses must override button_event()!')

    # return knob velocity as milliseconds between position changes (detents)
    # for backwards compatibility
    def vel_report(self):
        # print(self._velocity)
        return self._velocity


class GPIOEncoder(BaseEncoder):
    def __init__(self, pin_a, pin_b, pin_button=None, is_inverted=False, divisor=None):
        super().__init__(is_inverted)
        # Divisor can be 4 or 2 depending on whether the detent
        # on the encoder is defined by 2 or 4 pulses
        self.divisor = divisor

        self.pin_a = EncoderPin(pin_a)
        self.pin_b = EncoderPin(pin_b)
        self.pin_button = (
            EncoderPin(pin_button, button_type=True) if pin_button is not None else None
        )

        self._state = (self.pin_a.get_value(), self.pin_b.get_value())
        self._start_state = self._state

    def button_event(self):
        if self.pin_button:
            new_button_state = self.pin_button.get_value()
            if new_button_state != self._button_state:
                self._button_state = new_button_state
                if self.on_button_do is not None:
                    self.on_button_do(self.get_state())


class EncoderPin:
    def __init__(self, pin, button_type=False):
        self.pin = pin
        self.button_type = button_type
        self.prepare_pin()

    def prepare_pin(self):
        if self.pin is not None:
            self.io = digitalio.DigitalInOut(self.pin)
            self.io.direction = digitalio.Direction.INPUT
            self.io.pull = digitalio.Pull.DOWN
        else:
            self.io = None

    def get_value(self):
        return self.io.value


class EncoderDisplayHandler(Module):
    def __init__(self):
        self.encoders = []
        self.pins = None
        self.display = None
        self.encoder = None
        self.divisor = 4

    def on_runtime_enable(self, keyboard):
        return

    def on_runtime_disable(self, keyboard):
        return

    def during_bootup(self, keyboard):
        if self.pins and self.display:
            for idx, pins in enumerate(self.pins):
                try:
                    new_encoder = GPIOEncoder(*pins)
                    # Set default divisor if unset
                    if new_encoder.divisor is None:
                        new_encoder.divisor = self.divisor

                    # In our case, we need to define keybord and encoder_id for callbacks
                    new_encoder.on_move_do = lambda x, bound_idx=idx: self.on_move_do(
                        keyboard, bound_idx, x
                    )
                    new_encoder.on_button_do = (
                        lambda x, bound_idx=idx: self.on_button_do(
                            keyboard, bound_idx, x
                        )
                    )
                    self.encoders.append(new_encoder)
                except Exception as e:
                    print(e)
        return

    def on_move_do(self, keyboard, encoder_id, state):
        if self.display:
            layer_id = keyboard.active_layers[0]
            # if Left, key index 0 else key index 1
            self.display.clear()
            if state['direction'] == -1:
                self.display.showText('patras')
                self.encoder.prevLayer()
            else:
                self.display.showText('palante')
                self.encoder.nextLayer()
                
    def on_button_do(self, keyboard, encoder_id, state):
        if state['is_pressed'] is True:
            self.display.clear()
            self.display.showText('selecsion')

    def before_matrix_scan(self, keyboard):
        '''
        Return value will be injected as an extra matrix update
        '''
        for encoder in self.encoders:
            encoder.update_state()

        return keyboard

    def after_matrix_scan(self, keyboard):
        '''
        Return value will be replace matrix update if supplied
        '''
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

