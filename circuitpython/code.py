import time
import neopixel
import board
from digitalio import DigitalInOut, Direction, Pull

br = 0.3333
ch = 0.3333

pixel_ring_pin = board.D8
pixel_ring_num = 12

pixel_builtin       = board.NEOPIXEL #The neopixel can be accessed in this way
pixel_builtin_num   = 1 #only one pixel

pixel_builtin = neopixel.NeoPixel(pixel_builtin, pixel_builtin_num, brightness=0.05, auto_write=False)
pixel_ring = neopixel.NeoPixel(pixel_ring_pin, pixel_ring_num, brightness=0.1, auto_write=False, pixel_order=(1, 0, 2, 3))

btn1 = DigitalInOut(board.D1)
btn1.direction = Direction.INPUT
btn1.pull = Pull.UP

btn2 = DigitalInOut(board.D3)
btn2.direction = Direction.INPUT
btn2.pull = Pull.UP

def color_chase(color, wait):
    for i in range(pixel_ring_num):
        pixel_ring[i] = color
        time.sleep(wait)
        pixel_ring.show()
    time.sleep(0)

def colorwheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3, 0)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3, 0)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(pixel_ring_num):
            rc_index = (i * 256 // pixel_ring_num) + j
            pixel_ring[i] = colorwheel(rc_index & 255)
        pixel_ring.show()
        time.sleep(wait)

mode_prev_state = btn1.value
brgh_prev_state = btn2.value

nrOfModes = 4
currentMode = 0

modes = {
        0: ["Rainbow"],
        1: ["RED", (255, 0, 0, 0)], # RED
        2: ["GREEN", (0, 255, 0, 0)], # GREEN
        3: ["BLUE", (0, 0, 255, 0)]  # BLUE
}

while True:
    # Handle mode changes
    mode_cur_state = btn1.value
    if mode_cur_state != mode_prev_state:
        if mode_cur_state:
            currentMode += 1
            if currentMode >= nrOfModes:
                currentMode = 0
            print(modes[currentMode][0])
    
    mode_prev_state = mode_cur_state

    if currentMode == 0:    # Rainbow
        rainbow_cycle(0)
    elif currentMode == 1:  # Red
        color_chase(modes[currentMode][1], 0)
    elif currentMode == 2:  # Green
        color_chase(modes[currentMode][1], 0)
    elif currentMode == 3:  # Blue
        color_chase(modes[currentMode][1], 0)
    

    # Handle brightness changes
    brgh_cur_state = btn2.value
    
    if brgh_cur_state != brgh_prev_state:
        if brgh_cur_state:
            print(f"Brightness was: {br}", end="")
            br += ch
            if br >= 1:
                br = 0.0

            print(f", changed to: {br}")    
            pixel_ring.brightness = br
            pixel_ring.show()

    brgh_prev_state = brgh_cur_state