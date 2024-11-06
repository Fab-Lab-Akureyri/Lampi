import asyncio
import neopixel
import board
from digitalio import DigitalInOut, Direction, Pull

# LED setup
pixel_ring_pin = board.D6
pixel_ring_num = 12
pixel_ring = neopixel.NeoPixel(pixel_ring_pin, pixel_ring_num, brightness=0.3, auto_write=False, pixel_order=(1, 0, 2, 3))

# Button setup
btn1 = DigitalInOut(board.D1)
btn1.direction = Direction.INPUT
btn1.pull = Pull.UP

btn2 = DigitalInOut(board.D3)
btn2.direction = Direction.INPUT
btn2.pull = Pull.UP

# Brightness levels configuration
brightness_levels = [0.3, 0.6, 0.99]  # Desired brightness steps
current_brightness_index = 0  # Start at the first brightness level
breathing_task = None  # To manage breathing mode task

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

nrOfModes = 5
currentMode = 0

# Mode definitions with "OFF" mode added
modes = {
    0: ["OFF"],                     # OFF mode
    1: ["Rainbow"],                 # Rainbow mode
    2: ["RED", (255, 0, 0, 0)],     # RED
    3: ["GREEN", (0, 255, 0, 0)],   # GREEN
    4: ["BLUE", (0, 0, 255, 0)],    # BLUE
    5: ["WHITE", (0, 0, 0, 255)]    # WHITE
}

# Power-on white brightness sweep
async def power_on_sweep(pixel, pixel_number, duration=2):
    print("Running power on sweep")
    max_brightness = 0.5  # 50% brightness
    total_steps = 50  # Number of steps in the transition
    step_duration = duration / (total_steps * 2)  # Time per step, for both up and down

    for step in range(total_steps):
        brightness = (step / total_steps) * max_brightness
        white_value = int(255 * brightness)
        for i in range(pixel_number):
            pixel[i] = (0, 0, 0, white_value)
        pixel.show()
        await asyncio.sleep(step_duration)

    for step in range(total_steps, -1, -1):
        brightness = (step / total_steps) * max_brightness
        white_value = int(255 * brightness)
        for i in range(pixel_number):
            pixel[i] = (0, 0, 0, white_value)
        pixel.show()
        await asyncio.sleep(step_duration)

async def color_chase_a(color, interval):
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
            pixel.show()
            await asyncio.sleep(wait)

# Button monitoring with debouncing
async def monitor_button(btn, handler):
    prev_state = btn.value
    while True:
        current_state = btn.value
        if current_state != prev_state:
            prev_state = current_state
            if not current_state:
                await handler()
        await asyncio.sleep(0.01)

# Continuous breathing mode effect
async def breathing_mode():
    global brightness_levels, current_brightness_index
    print("Entering continuous breathing mode...")

    # Define breathing parameters
    breath_steps = 50  # Number of steps for each breath in and out
    max_brightness = 0.99  # Maximum brightness for breathing effect
    min_brightness = 0.3  # Minimum brightness for breathing effect
    duration = 2.0  # Total time for one breath cycle

    while True:
        # Increase brightness (inhale)
        for step in range(breath_steps):
            brightness = min_brightness + ((max_brightness - min_brightness) * step / breath_steps)
            pixel_ring.brightness = brightness
            pixel_ring.show()
            await asyncio.sleep(duration / (2 * breath_steps))

        # Decrease brightness (exhale)
        for step in range(breath_steps, -1, -1):
            brightness = min_brightness + ((max_brightness - min_brightness) * step / breath_steps)
            pixel_ring.brightness = brightness
            pixel_ring.show()
            await asyncio.sleep(duration / (2 * breath_steps))

# Handlers for button press events
async def handle_btn1_press():
    global currentMode, rainbow_task, modes, breathing_task

    # Switch to the next mode
    currentMode += 1
    if currentMode >= len(modes):
        currentMode = 0

    print(f"Switching to mode: {modes[currentMode][0]}")

    # Stop rainbow task if it's running
    if rainbow_task and not rainbow_task.done():
        rainbow_task.cancel()
        rainbow_task = None

    # Stop breathing task if switching to OFF mode
    if currentMode == 0:  # OFF mode
        if breathing_task and not breathing_task.done():
            breathing_task.cancel()
            breathing_task = None
        pixel_ring.fill((0, 0, 0, 0))
        pixel_ring.show()
        return  # Exit function early for OFF mode

    # If breathing mode is active, keep it running for the new mode
    if breathing_task and not breathing_task.done():
        # Update the mode but continue breathing
        if currentMode == 1:  # Rainbow mode
            rainbow_task = asyncio.create_task(rainbow_cycle_a(pixel_ring, pixel_ring_num, 0.01))
        else:
            color = modes[currentMode][1]
            asyncio.create_task(color_chase_a(color, 0.01))
    else:
        # Start the color chase or rainbow cycle without breathing if it's not active
        if currentMode == 1:
            rainbow_task = asyncio.create_task(rainbow_cycle_a(pixel_ring, pixel_ring_num, 0.01))
        else:
            color = modes[currentMode][1]
            asyncio.create_task(color_chase_a(color, 0.01))

async def handle_btn2_press():
    global current_brightness_index, brightness_levels, breathing_task

    # If breathing mode is active, cancel it before changing brightness
    if breathing_task and not breathing_task.done():
        breathing_task.cancel()
        breathing_task = None
        # Reset brightness to the initial level after breathing mode ends
        current_brightness_index = 0  # Reset to 0.3 after breathing
    else:
        # Cycle through brightness levels
        if current_brightness_index < len(brightness_levels) - 1:
            # Move to the next brightness level
            current_brightness_index += 1
        else:
            # Enter breathing mode if at max brightness level
            breathing_task = asyncio.create_task(breathing_mode())
            return  # Exit to let breathing mode take over

    # Explicitly set brightness to ensure it starts at 0.3 after breathing mode
    pixel_ring.brightness = brightness_levels[current_brightness_index]
    pixel_ring.show()
    print(f"Brightness is now: {pixel_ring.brightness}")

# Main function
async def main():
    # Explicitly set initial brightness to 0.3 on startup
    pixel_ring.brightness = brightness_levels[0]
    await power_on_sweep(pixel_ring, pixel_ring_num)

    btn1_monitor = asyncio.create_task(monitor_button(btn1, handle_btn1_press))
    btn2_monitor = asyncio.create_task(monitor_button(btn2, handle_btn2_press))
    
    await asyncio.gather(btn1_monitor, btn2_monitor)

asyncio.run(main())
