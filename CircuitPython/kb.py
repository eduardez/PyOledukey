import board
import busio
import digitalio

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners.digitalio import MatrixScanner
from kmk.scanners import DiodeOrientation

from micropython_pcf8575 import PCF8575

def generatePin(pinnum, pcf):
    pin_ = pcf.get_pin(pinnum)
    pin_.switch_to_input()
    pin_.direction = digitalio.Direction.INPUT
    return pin_

class KMKKeyboard(_KMKKeyboard):
    # I2C IO EXPANDER PCF8574
    # i2c = busio.I2C(scl=board.GP10, sda=board.GP11, frequency=100000)

    row_pins = [
        board.GP5,
        board.GP6,
        board.GP7,
        board.GP8,
        board.GP9
    ]
    
    
    col_pins = [
        board.GP0,
        board.GP1,
        board.GP2,
        board.GP3,
        board.GP4,
        board.GP10,
        board.GP11,
        board.GP21,
        board.GP22,
        board.GP26,
        board.GP27,
        board.GP28
    ]
    
    diode_orientation = DiodeOrientation.ROW2COL
    matrix = MatrixScanner(
            cols=col_pins,
            rows=row_pins,
            diode_orientation=diode_orientation,
            rollover_cols_every_rows=None, # optional
    )
