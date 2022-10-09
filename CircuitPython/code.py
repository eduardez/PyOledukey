# Base
import board
import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_sh1106
import time

# KMK
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.modtap import ModTap
#from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys

# Own
from src.customEncoder import EncoderHandler, GPIOEncoder
from src.oledController import OledController
from src.menuController import MenuControllerHandler, MenuController, MenuItem
from kb import KMKKeyboard
from images import volume

# ========== INITIALIZATION ==========
# --- Keyboard
keyboard = KMKKeyboard()
keyboard.tap_time = 150

# --- Encoder
action_encoder_handler = EncoderHandler() 
menu_controller_handler = MenuControllerHandler() 

# --- Modules
modtap = ModTap()
layers_ext = Layers()
media_keys = MediaKeys()

keyboard.modules = [layers_ext, modtap, action_encoder_handler, menu_controller_handler]
keyboard.extensions = [media_keys]

# --- Display
displayio.release_displays()

display_spi = busio.SPI(board.GP18, board.GP19)
display_bus = displayio.FourWire(
    display_spi,
    command=board.GP17,
    chip_select=board.GP16,
    reset=board.GP20,
    baudrate=1000000,
)


# ========== VALUES ==========
# --- Display
WIDTH = 128
HEIGHT = 64

oled = OledController(display_bus, WIDTH, HEIGHT)

# --- Encoder
menu_controller_encoder = GPIOEncoder(board.GP12, board.GP13, None, True, 2)
action_encoder = GPIOEncoder(board.GP14, board.GP15, None, True, 2)

# --- Action controller
action_encoder_handler.encoder = action_encoder

# --- Menu Controller
menu_controller_instance = MenuController(oled, action_encoder_handler)
menu_controller_instance.setMenuList([
    MenuItem("vol", "Volumen", volume.ANIMATION, (KC.VOLD, KC.VOLU, KC.MUTE)),
    MenuItem("bright", "Brillo", None, (KC.BRID, KC.BRIU, KC.MUTE)),
    MenuItem("media", "Media", None, (KC.MPRV, KC.MNXT, KC.MPLY)),
    MenuItem("other", "Otros", None, None),
])
menu_controller_instance.setMenuIndex(0) 

# --- Menu Controller handler
menu_controller_handler.display = oled
menu_controller_handler.menu_encoder = menu_controller_encoder
menu_controller_handler.action_encoder_handler = action_encoder_handler
menu_controller_handler.menu_controller = menu_controller_instance



# ========== KEY MAPPING ==========

# Cleaner key nameseqpitew
_______ = KC.TRNS
XXXXXXX = KC.NO

LOWER = KC.MO(1)
# RAISE = KC.MO(2)

# --- Keyboard
keyboard.keymap = [
    #[  #QWERTY
    #    KC.ESC,   KC.N1,  KC.N2,   KC.N3,   KC.N4,   KC.N5,                    KC.N6,   KC.N7,
    #    KC.TAB,   KC.Q,   KC.W,    KC.E,    KC.R,    KC.T,                     KC.Y,    KC.U,
    #    KC.LCTRL, KC.A,   KC.S,    KC.D,    KC.F,    KC.G,                     KC.H,    KC.J,
    #    KC.LSFT,  KC.Z,   KC.X,    KC.C,    KC.V,    KC.B,                     KC.N,    KC.M,
    #    KC.LSFT,  KC.Z,   KC.X,    KC.C,    KC.V,    KC.B,                     KC.N,    KC.M,
    #],
     [  #QWERTY
         KC.ESC,   KC.N1,     KC.N2,      KC.N3,   KC.N4,   KC.N5,            KC.N6,   KC.N7,   KC.N8,   KC.N9,    KC.N0,   LOWER,
         KC.TAB,   KC.Q,      KC.W,       KC.E,    KC.R,    KC.T,             KC.Y,    KC.U,    KC.I,    KC.O,     KC.P,    KC.MINS,
         KC.CAPS,  KC.A,      KC.S,       KC.D,    KC.F,    KC.G,             KC.H,    KC.J,    KC.K,    KC.L,     KC.SCLN, KC.LBRC,
         KC.LSFT,  KC.Z,      KC.X,       KC.C,    KC.V,    KC.B,             KC.N,    KC.M,    KC.N,    KC.QUOT,  KC.UP,   KC.RBRC,
         KC.LCTRL, KC.LWIN,   KC.LALT,    KC.QUES,    KC.SCOLON,  KC.SPACE,   KC.BACKSPACE,    KC.M,    KC.V,    KC.LEFT,  KC.DOWN, KC.RIGHT
     ],
     
     [  #QWERTY
         KC.XXXXXXX,   KC.XXXXXXX,     KC.XXXXXXX,      KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,            KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,
         KC.XXXXXXX,   KC.XXXXXXX,     KC.XXXXXXX,      KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,            KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,
         KC.XXXXXXX,   KC.XXXXXXX,     KC.XXXXXXX,      KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,            KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,
         KC.XXXXXXX,   KC.XXXXXXX,     KC.XXXXXXX,      KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,            KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,
         KC.XXXXXXX,   KC.XXXXXXX,     KC.SLSH,      KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,            KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX
    ],
    # [  #QWERTY
    #      KC.XXXXXXX,   KC.XXXXXXX,     KC.XXXXXXX,      KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,            KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,
    #      KC.XXXXXXX,   KC.XXXXXXX,     KC.XXXXXXX,      KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,            KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,
    #      KC.XXXXXXX,   KC.XXXXXXX,     KC.XXXXXXX,      KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,            KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,
    #      KC.XXXXXXX,   KC.XXXXXXX,     KC.XXXXXXX,      KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,            KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,
    #      KC.XXXXXXX,   KC.XXXXXXX,     KC.XXXXXXX,      KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,            KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX,   KC.XXXXXXX
    # ],
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


# ========== RUN KEYBOARD ==========
keyboard.debug_enabled = True
keyboard.go()
