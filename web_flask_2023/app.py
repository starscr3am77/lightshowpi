import sys
from flask import Flask, request, render_template, redirect, url_for, flash
import os
import subprocess
import logging
from time import sleep
import shlex
from subprocess import Popen

app = Flask(__name__)


app.secret_key = 'DSAREYUIY%$#$%^TREWSRYU876543'

# Configure Logger
logger = logging.getLogger("lightshowpi")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Set environment variables
HOME = os.environ.get('SYNCHRONIZED_LIGHTS_HOME', '/home/pi/lightshow2022')
BROADLINK = os.environ.get('BROADLINK', '/home/pi/Projects/broadlink')

# Importing send_commands module (Adjust the path as per your environment)
sys.path.append(BROADLINK)
import send_commands

def connect():
    try:
        connection = send_commands.connect("localhost", port=39554)
        logger.info("Connected to local relay server")
        return connection
    except Exception as e:
        logger.warning(f"Couldn't connect to server: {e}")
        return False

@app.route('/')
def root():
    return redirect(url_for('index'))


@app.route('/lightshowpi/', methods=['GET', 'POST'])
@app.route('/lightshowpi', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form.get('message')
        execute_command(message)
        # Redirect to the external URL
        flash(f'Command "{message}" executed successfully!', 'success')  # Send a flash message
        return redirect(url_for('index', _external=True))

    # For GET request or initial load
    return render_template('index.html')

def execute_command(command):
    connection = connect()
    if command == "On":
        kill_processes()
        os.system(f"python {HOME}/py/hardware_controller.py --state=on")
    elif command == "Off":
        kill_processes()
        os.system(f"python {HOME}/py/hardware_controller.py --state=off")
    elif command == "Next":
        kill_processes()
        sleep(1)
    elif command == "Speakers On":
        if connection:
            send_commands.send_command_server(connection, "Speakers", "on", confirm=False)
    elif command == "Speakers Off":
        if connection:
            send_commands.send_command_server(connection, "Speakers", "off", confirm=False)
    elif command == "System Off":
        if connection:
            send_commands.send_command_server(connection, "Speakers", "off", confirm=False)
        kill_processes()
    elif command == "Start":
        #kill_processes()
        #os.system(f"{HOME}/bin/play_sms &")
        #os.system(f"{HOME}/bin/check_sms &")
        connection = connect()
        if connection:
            send_commands.send_command_server(connection, "Speakers", "on", confirm=False)
            logger.info("Sent command to turn on speakers (part of Start)")
        os.system('pkill -f "bash $SYNCHRONIZED_LIGHTS_HOME/bin"')
        os.system('pkill -f "python $SYNCHRONIZED_LIGHTS_HOME/py"')
        os.system("${SYNCHRONIZED_LIGHTS_HOME}/bin/play_sms &")
        os.system("${SYNCHRONIZED_LIGHTS_HOME}/bin/check_sms &")

def kill_processes():
    os.system(f'pkill -f "bash {HOME}/bin"')
    os.system(f'pkill -f "python {HOME}/py"')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8283)

