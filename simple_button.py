import RPi.GPIO as GPIO
import time
import subprocess

BUTTON_PIN = 21  # or any GPIO pin you choose

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("Waiting for button press to start lightshow...")

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
            print("Button pressed! Starting lightshow...")
            subprocess.run(["sudo", "python3", "/home/pi/lightshowpi/py/synchronized_lights.py"])
            break
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Stopped by user.")
finally:
    GPIO.cleanup()
