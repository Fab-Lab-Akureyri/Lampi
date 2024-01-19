# Jani mill
# x = com15
# y = com18
# z = com17

# r = com8

#import time
#import neopixel
#import board
##s = serial.Serial('COM8')
#import select
#import sys
#
#led = neopixel.NeoPixel(board.NEOPIXEL, 1)
#
#poll_object = select.poll()
#poll_object.register(sys.stdin,1)
#
#timeout = 0.05
#
#while True:
#    #ch = sys.stdin.read(1)
#    #print (ch,"hello from the pico")
#    #print("RP2040 connected")
#    #time.sleep(2)
#
##    #print("asdf")
#    #if select.select([sys.stdin],[],[],0)[0]:
#    #    ch = sys.stdin.readline()
#    #    print(ch)
#    if poll_object.poll(0):
#        #read as character
#        ch = sys.stdin.read(1)
#        # print (ch,"hello from the pico")
#        if ch == "f":
#            print (f"Recieved: {ch}")
#            led[0] = (124, 0, 0)
#            time.sleep(timeout)
#            led[0] = (0, 0, 0)
#        elif ch == "b":
#            print (f"Recieved: {ch}")
#            led[0] = (0, 124, 0)
#            time.sleep(timeout)
#            led[0] = (0, 0, 0)
#        elif ch == "r":
#            print (f"Recieved: {ch}")
#            led[0] = (0, 0, 124)
#            time.sleep(timeout)
#            led[0] = (0, 0, 0)
#
#            
#import usb_hid
#from adafruit_hid.keyboard import Keyboard
#import time
#
#from adafruit_hid.keycode import Keycode
#from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
#
#
## Set up a keyboard device.
#kbd = Keyboard(usb_hid.devices)
#layout = KeyboardLayoutUS(kbd)
#kbd.send(Keycode.WINDOWS)
#time.sleep(0.5)
#layout.write('notepad')
#time.sleep(0.5)
#kbd.send(Keycode.ENTER)
#time.sleep(2)
#layout.write('Doddi er flottur og Arni er bestur!\n')


import time
#from tkinter import colorchooser
import neopixel
import board
import digitalio
import asyncio
import countio
from adafruit_debouncer import Debouncer

btn_1 = board.D1
btn_2 = board.D3

pixel_ring_pin = board.D8
pixel_ring_num = 12

pixel_builtin       = board.NEOPIXEL #The neopixel can be accessed in this way
pixel_builtin_num   = 1 #only one pixel

pixel_builtin = neopixel.NeoPixel(pixel_builtin, pixel_builtin_num, brightness=0.05, auto_write=False)

br = 0.1
ch = 0.2

pixel_ring = neopixel.NeoPixel(pixel_ring_pin, pixel_ring_num, brightness=0.1, auto_write=False, pixel_order=(1, 0, 2, 3))

async def catch_interrupt_1(pin):
    """Print a message when pin goes low."""
    with countio.Counter(pin) as interrupt:
        while True:
            if interrupt.count > 0:
                interrupt.count = 0
                print("Interrupt 1, breyta birtu!")
                global pixel_ring
                global br
                global ch

                br += ch
                if br >= 1:
                    br = 0.1

                print("Britustig: ", end ="")
                print(br)
                pixel_ring.brightness = br
                pixel_ring.show()
                pixel_builtin.brightness = br
                pixel_builtin.show()
            # Let another task run.
            await asyncio.sleep(0)

async def catch_interrupt_2(pin):
    """Print a message when pin goes low."""
    with countio.Counter(pin) as interrupt:
        while True:
            if interrupt.count > 0:
                interrupt.count = 0
                print("Maggi flotti 2, breyta birtu!")
                global pixel_ring
                global br
                global ch

                br += ch
                if br >= 1:
                    br = 0.1

                print("Britustig: ", end ="")
                print(br)
                pixel_ring.brightness = br
                pixel_ring.show()
                pixel_builtin.brightness = br
                pixel_builtin.show()
            # Let another task run.
            await asyncio.sleep(0)

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

async def color_chase_a(color, wait, interval):
    await asyncio.sleep(wait)
    for i in range(pixel_ring_num):
        pixel_ring[i] = color
        await asyncio.sleep(interval)
        pixel_ring.show()

def color_chase(color, wait):
    for i in range(pixel_ring_num):
        pixel_ring[i] = color
        time.sleep(wait)
        pixel_ring.show()
    time.sleep(0.5)

def rainbow_cycle(wait):
    print("hgdf")
    for j in range(255):
        for i in range(pixel_ring_num):
            rc_index = (i * 256 // pixel_ring_num) + j
            pixel_ring[i] = colorwheel(rc_index & 255)
        pixel_ring.show()
        time.sleep(wait)

async def rainbow_cycle_a(pixel, pixel_number, wait):
    while True:
        for j in range(255):
            for i in range(pixel_number):
                rc_index = (i * 256 // pixel_number) + j
                pixel[i] = colorwheel(rc_index & 255)
            pixel.show()
            await asyncio.sleep(wait)

RED = (255, 0, 0, 0)
YELLOW = (255, 150, 0, 0)
GREEN = (0, 255, 0, 0)
CYAN = (0, 255, 255, 0)
BLUE = (0, 0, 255, 0)
PURPLE = (180, 0, 255, 0)

async def test():
    while True:
        print("Hallo Fab Lab - þetta virkar rosa vel!")
        pixel_builtin.brightness = 0.1
        pixel_builtin.show()
        await asyncio.sleep(5)

async def btntest1(pin):
    print("Hallo from btn 1!")
    await asyncio.sleep(1)


async def btntest2(pin):
    print("Hallo from btn 2!")
    await asyncio.sleep(1)

async def main():
    interrupt_task_1 = asyncio.create_task(catch_interrupt_1(btn_1))
    interrupt_task_2 = asyncio.create_task(catch_interrupt_2(btn_2))
    
    test_task00 = asyncio.create_task(rainbow_cycle_a(pixel_builtin, pixel_builtin_num, 0))
    test_task01 = asyncio.create_task(rainbow_cycle_a(pixel_ring, pixel_ring_num, 0))
    
    #lower_brightness_task = asyncio.create_task(test())

    #await asyncio.gather(interrupt_task_1, interrupt_task_2, test_task00, test_task01)
    await asyncio.gather(interrupt_task_1, interrupt_task_2)

asyncio.run(main())
