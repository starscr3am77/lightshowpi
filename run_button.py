import RPi.GPIO as GPIO
import subprocess
import time
import os

# Configuration
BUTTON_GPIO = 21
SCRIPT_PATH = os.path.expanduser("~/Documents/lightshowpi/py/synchronized_lights.py")
DEBOUNCE_TIME = 300  # milliseconds

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# State variable to track running script
script_process = None

def button_pressed(channel):
    global script_process
    if script_process is None or script_process.poll() is not None:
        print("Button pressed, starting lightshow...")
        script_process = subprocess.Popen(["python3", SCRIPT_PATH])
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
