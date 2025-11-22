#!/usr/bin/env python
"""
Button Controller for LightShowPi
Monitors a physical button to start/stop the lightshow

Author: AI Assistant
"""

import RPi.GPIO as GPIO
import time
import subprocess
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
BUTTON_GPIO = 21  # GPIO pin number (BCM numbering)
DEBOUNCE_TIME = 0.3  # seconds to wait to avoid button bounce
LIGHTSHOW_RUNNING = False

# Get LightShowPi home directory
LIGHTSHOW_HOME = os.environ.get('SYNCHRONIZED_LIGHTS_HOME', '/home/pi/lightshowpi')

def setup_button():
    """Initialize GPIO for button input"""
    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    logger.info(f"Button initialized on GPIO {BUTTON_GPIO}")

def is_lightshow_running():
    """Check if synchronized_lights.py is currently running"""
    try:
        result = subprocess.run(
            ['pgrep', '-f', 'synchronized_lights.py'],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        logger.error(f"Error checking lightshow status: {e}")
        return False

def start_lightshow():
    """Start the lightshow"""
    try:
        logger.info("Starting lightshow...")
        # You can customize this command based on your needs
        # Option 1: Start with default playlist
        cmd = [
            'sudo', 'python',
            f'{LIGHTSHOW_HOME}/py/synchronized_lights.py',
            '--mode=audio-in'
        ]
        
        # Option 2: Start with specific playlist (uncomment if preferred)
        # cmd = [
        #     'sudo', 'python',
        #     f'{LIGHTSHOW_HOME}/py/synchronized_lights.py',
        #     f'--playlist={LIGHTSHOW_HOME}/music/sample/.playlist'
        # ]
        
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=LIGHTSHOW_HOME
        )
        logger.info("Lightshow started successfully")
        return True
    except Exception as e:
        logger.error(f"Error starting lightshow: {e}")
        return False

def stop_lightshow():
    """Stop the lightshow"""
    try:
        logger.info("Stopping lightshow...")
        subprocess.run(['sudo', 'pkill', '-f', 'synchronized_lights.py'])
        time.sleep(1)
        # Turn off all channels
        subprocess.run([
            'sudo', 'python',
            f'{LIGHTSHOW_HOME}/py/on_or_off.py',
            '--state=off'
        ])
        logger.info("Lightshow stopped successfully")
        return True
    except Exception as e:
        logger.error(f"Error stopping lightshow: {e}")
        return False

def button_pressed_callback(channel):
    """Called when button is pressed"""
    global LIGHTSHOW_RUNNING
    
    # Debounce - wait a bit and check if still pressed
    time.sleep(0.05)
    if GPIO.input(BUTTON_GPIO) != GPIO.LOW:
        return  # False trigger
    
    logger.info("Button pressed!")
    
    # Toggle lightshow on/off
    if is_lightshow_running():
        logger.info("Lightshow is running - stopping it")
        stop_lightshow()
        LIGHTSHOW_RUNNING = False
    else:
        logger.info("Lightshow is not running - starting it")
        start_lightshow()
        LIGHTSHOW_RUNNING = True
    
    # Wait for button release to avoid multiple triggers
    while GPIO.input(BUTTON_GPIO) == GPIO.LOW:
        time.sleep(0.1)

def main():
    """Main function - monitors button continuously"""
    try:
        setup_button()
        
        # Add event detection for button press (falling edge = button pressed)
        GPIO.add_event_detect(
            BUTTON_GPIO,
            GPIO.FALLING,
            callback=button_pressed_callback,
            bouncetime=int(DEBOUNCE_TIME * 1000)  # convert to milliseconds
        )
        
        logger.info("Button controller started. Press button to toggle lightshow.")
        logger.info("Press Ctrl+C to exit")
        
        # Keep the script running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Button controller stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        GPIO.cleanup()
        logger.info("GPIO cleaned up")

if __name__ == '__main__':
    main()
