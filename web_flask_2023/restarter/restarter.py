import os
import time
import subprocess

signal_file = '/home/pi/lightshow2022/web_flask_2023/restarter/restart_signal.txt'
flask_app = '/home/pi/lightshow2022/web_flask_2023/app.py'

while True:
    if os.path.exists(signal_file):
        os.remove(signal_file)  # Remove the signal file
        # Restart the Flask app
        subprocess.run(['pkill', '-f', flask_app])  # Kill current Flask app
        time.sleep(2)  # Wait for the app to fully terminate
        subprocess.run(['python', flask_app])  # Start Flask app

    time.sleep(5)  # Check every 5 seconds

