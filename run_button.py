import RPi.GPIO as GPIO
import subprocess
import time
import os
import psutil  # Requires: pip3 install psutil

# Configuration
BUTTON_GPIO = 21
SCRIPT_PATH = "/home/pi/Documents/lightshowpi/py/synchronized_lights.py"
DEBOUNCE_TIME = 300  # milliseconds

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def is_script_running(script_name):
    """Check if script is running anywhere in the system process list."""
    for proc in psutil.process_iter(['cmdline']):
        try:
            if script_name in ' '.join(proc.info['cmdline']):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

def button_pressed(channel):
    if not is_script_running("synchronized_lights.py"):
        print("Button pressed, starting lightshow...")
        subprocess.Popen(["python3", SCRIPT_PATH])
    else:
        print("Button press ignored, lightshow already running.")

# Attach interrupt with debounce
GPIO.add_event_detect(BUTTON_GPIO, GPIO.RISING, callback=button_pressed, bouncetime=DEBOUNCE_TIME)

print("Waiting for button press. Press Ctrl+C to exit.")
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
