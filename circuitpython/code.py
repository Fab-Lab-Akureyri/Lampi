import asyncio
import neopixel
import board
from digitalio import DigitalInOut, Direction, Pull

# LED setup
pixel_ring_pin = board.D8
pixel_ring_num = 12
pixel_ring = neopixel.NeoPixel(pixel_ring_pin, pixel_ring_num, brightness=0.3333, auto_write=False, pixel_order=(1, 0, 2, 3))

# Button setup
btn1 = DigitalInOut(board.D1)
btn1.direction = Direction.INPUT
btn1.pull = Pull.UP

btn2 = DigitalInOut(board.D3)
btn2.direction = Direction.INPUT
btn2.pull = Pull.UP

# State variables
mode_prev_state = btn1.value
brgh_prev_state = btn2.value
nrOfModes = 4
currentMode = 0
br = 0.3333
ch = 0.3333

rainbow_task = None  # Task to manage the rainbow cycle

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

# Mode definitions with "OFF" mode added
modes = {
    0: ["OFF"],                     # OFF mode
    1: ["Rainbow"],                 # Rainbow mode
    2: ["RED", (255, 0, 0, 0)],     # RED
    3: ["GREEN", (0, 255, 0, 0)],   # GREEN
    4: ["BLUE", (0, 0, 255, 0)]     # BLUE
}

# Power-on color sweep
async def power_on_sweep(pixel, pixel_number):
    for j in range(255):
        for i in range(pixel_number):
            rc_index = (i * 256 // pixel_number) + j
            pixel[i] = colorwheel(rc_index & 255)
        pixel.show()
        await asyncio.sleep(0.01)  # Adjust speed as needed
    for i in range(pixel_number):  # Turn off all pixels after the sweep
        pixel[i] = (0, 0, 0, 0)
    pixel.show()

async def color_chase_a(color, wait, interval):
    await asyncio.sleep(wait)
    for i in range(pixel_ring_num):
        pixel_ring[i] = color
        await asyncio.sleep(interval)
        pixel_ring.show()

async def rainbow_cycle_a(pixel, pixel_number, wait):
    while True:
        for j in range(255):
            for i in range(pixel_number):
                rc_index = (i * 256 // pixel_number) + j
                pixel[i] = colorwheel(rc_index & 255)
            pixel.show()  # Update the entire strip at once
            await asyncio.sleep(wait),

# Button monitoring with debouncing
async def monitor_button(btn, handler):
    prev_state = btn.value
    while True:
        current_state = btn.value
        if current_state != prev_state:
            prev_state = current_state
            if not current_state:
                await handler()
        await asyncio.sleep(0.01)  # Debounce time

# Handlers for button press events
async def handle_btn1_press():
    global currentMode, rainbow_task, modes
    currentMode += 1
    if currentMode >= len(modes):
        currentMode = 0

    print(f"Switching to mode: {modes[currentMode][0]}")  # Logging the mode change
    
    # Handle the OFF mode separately
    if currentMode == 0:  # OFF mode
        pixel_ring.fill((0, 0, 0, 0))
        pixel_ring.show()
        if rainbow_task and not rainbow_task.done():
            rainbow_task.cancel()
            rainbow_task = None
        return  # Exit the handler early

    # Manage the rainbow_task based on the current mode
    if currentMode == 1:  # Rainbow mode
        if rainbow_task is None or rainbow_task.done():
            rainbow_task = asyncio.create_task(rainbow_cycle_a(pixel_ring, pixel_ring_num, 0.01))
    else:  # Red, Green, or Blue mode
        if rainbow_task and not rainbow_task.done():
            rainbow_task.cancel()
            rainbow_task = None
        # Start the color chase for the respective color
        color = modes[currentMode][1]
        asyncio.create_task(color_chase_a(color, 0, 0.01))

async def handle_btn2_press():
    global br, ch
    br += ch
    if br >= 1:
        br = 0.3333
    pixel_ring.brightness = br
    pixel_ring.show()

# Main function
async def main():
    # Start with a power-on color sweep
    await power_on_sweep(pixel_ring, pixel_ring_num)
    
    btn1_monitor = asyncio.create_task(monitor_button(btn1, handle_btn1_press))
    btn2_monitor = asyncio.create_task(monitor_button(btn2, handle_btn2_press))
    
    await asyncio.gather(btn1_monitor, btn2_monitor)

# Run the main function
asyncio.run(main())