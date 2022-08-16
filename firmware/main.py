from kb import KMKKeyboard

from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.modtap import ModTap

# KEYBOARD
keyboard = KMKKeyboard()

modtap = ModTap()
layers_ext = Layers()

keyboard.modules = [layers_ext, modtap]

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

# LOWER = KC.MO(1)
# RAISE = KC.MO(2)

# --------------- EXTRA -----------------
keyboard.debug_enabled = True

keyboard.keymap = [
    #[  #QWERTY
    #    KC.ESC,   KC.N1,  KC.N2,   KC.N3,   KC.N4,   KC.N5,                    KC.N6,   KC.N7,
    #    KC.TAB,   KC.Q,   KC.W,    KC.E,    KC.R,    KC.T,                     KC.Y,    KC.U,
    #    KC.LCTRL, KC.A,   KC.S,    KC.D,    KC.F,    KC.G,                     KC.H,    KC.J,
    #    KC.LSFT,  KC.Z,   KC.X,    KC.C,    KC.V,    KC.B,                     KC.N,    KC.M,
    #    KC.LSFT,  KC.Z,   KC.X,    KC.C,    KC.V,    KC.B,                     KC.N,    KC.M,
    #],
     [  #QWERTY
         KC.ESC,   KC.N1,  KC.N2,   KC.N3,   KC.N4,   KC.N5,                    KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.GRV,
         KC.TAB,   KC.Q,   KC.W,    KC.E,    KC.R,    KC.T,                     KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.MINS,
         KC.LCTRL, KC.A,   KC.S,    KC.D,    KC.F,    KC.G,                     KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, KC.QUOT,
         KC.LSFT,  KC.Z,   KC.X,    KC.C,    KC.V,    KC.B,                     KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, KC.RSFT,
         KC.LSFT,  KC.N1,   KC.X,    KC.C,    KC.V,    KC.B,                     KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, KC.RSFT
     ],
    # [  #LOWER
    #     KC.F1,  KC.F2,    KC.F3,   KC.F4,   KC.F5,   KC.F6,                     KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.F12,
    #     KC.GRV, KC.EXLM,  KC.AT,   KC.HASH, KC.DLR,  KC.PERC,                   KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, KC.TILD,
    #     _______, _______, _______, _______, _______, _______, _______, _______, XXXXXXX, KC.UNDS, KC.PLUS, KC.LCBR, KC.RCBR, KC.PIPE,
    #                                _______, _______, _______, _______, _______, _______, _______, _______
    # ],
    # [  #RAISE
    #     KC.GRV, KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,                       KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   _______,
    #     KC.F1,  KC.F2,   KC.F3,   KC.F4,   KC.F5,   KC.F6,                       XXXXXXX, KC.LEFT, KC.DOWN, KC.UP,   KC.RGHT, XXXXXXX,
    #     KC.F7,  KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.F12,   _______, _______,  KC.PLUS, KC.MINS, KC.EQL,  KC.LBRC, KC.RBRC, KC.BSLS,
    #                               _______, _______, _______,  _______, _______,  _______, _______, _______
    # ]
]

if __name__ == '__main__':
    keyboard.go()
