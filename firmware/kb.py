import board
import busio
import digitalio

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners.digitalio import MatrixScanner
from kmk.scanners import DiodeOrientation

from micropython_pcf8575 import PCF8575

def generatePin(pinnum, pcf):
    pin_ = pcf.get_pin(pinnum)
    pin_.switch_to_output(value=False)
    pin_.direction = digitalio.Direction.OUTPUT
    return pin_

class KMKKeyboard(_KMKKeyboard):
    # I2C IO EXPANDER PCF8574
    # i2c = busio.I2C(scl=board.GP10, sda=board.GP11, frequency=100000)
    
    i2c = busio.I2C(scl=board.GP11, sda=board.GP10)
    i2c.unlock()
    pcf = PCF8575(i2c, address=0x20)


    row_pins = [
        board.GP5,
        board.GP6,
        board.GP7,
        board.GP8,
        board.GP9
    ]
    
    col_pins = [
        generatePin(0, pcf),
        generatePin(1, pcf),
        generatePin(2, pcf),
        generatePin(3, pcf),
        generatePin(4, pcf),
        generatePin(5, pcf),
        generatePin(6, pcf),
        generatePin(7, pcf),
        generatePin(8, pcf),
        generatePin(9, pcf),
        generatePin(10, pcf),
        generatePin(11, pcf),
    ]
    
    diode_orientation = DiodeOrientation.COL2ROW
    matrix = MatrixScanner(
            cols=col_pins,
            rows=row_pins,
            diode_orientation=diode_orientation,
            rollover_cols_every_rows=None, # optional
    )
