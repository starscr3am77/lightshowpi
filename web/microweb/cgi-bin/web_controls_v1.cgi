#!/usr/bin/python

#
# Licensed under the BSD license.  See full license in LICENSE file.
# http://www.lightshowpi.org/
#
# Author: Ken B

import cgi
import cgitb
import os
from time import sleep
import sys
import logging
import html
from pathlib import Path
import datetime
from collections import deque
import subprocess, signal

# This script is run by SUDO! Make sure sudo python has the appropriate libraries, paths, etc.
# Does not appear to use crontab environment
# Broadlink path set in /etc/sudoers
# Defaults        env_keep=SYNCHRONIZED_LIGHTS_HOME
# Defaults        env_keep+=BROADLINK

broadlink2 = "/home/pi/broadlink"
broadlink = os.getenv("BROADLINK")
sys.path.append(broadlink)
sys.path.append(broadlink2)

logger = logging.getLogger("root")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info(broadlink)
logger.info(sys.version_info)
HOME=os.environ['SYNCHRONIZED_LIGHTS_HOME']

import send_commands

def connect():
    try:
        connection = send_commands.connect("localhost", port=39554)
        logger.info("Connected to local relay server")
        return connection
    except:
        return False

if False:
    try:
        # Connect directly to Pi
        if False:
            connection = send_commands.connect("192.168.187.103", 32001)
            #connection = send_commands.connect("fife.entrydns.org", 57325)
        else:
            # Connect to local thing
            connection = send_commands.connect("localhost", port=39554)
            logger.info("Connected to local relay")

        no_connection=False
    except:
        no_connection=True
        logger.warning("Couldn't connect to server")
else:
    no_connection = True

cgitb.enable()  # for troubleshooting
form = cgi.FieldStorage()
message = form.getvalue("message", "")

print("Content-type: text/html")

print("""
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>LightShowPi Web Controls</title>
        <meta name="description" content="A very basic web interface for LightShowPi">
        <meta name="author" content="Ken B">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="shortcut icon" href="/favicon.png">
        <meta name="mobile-web-app-capable" content="yes">
        <link rel="icon" sizes="196x196" href="/favicon.png">
        <link rel="apple-touch-icon" sizes="152x152" href="/favicon.png">
        <link rel="stylesheet" href="/css/style.css">
    </head>
    <body>
        <center>
            <h1> LightShowPi Web Controls </h1>

            <form method="post" action="web_controls.cgi">
                <input type="hidden" name="message" value="On"/>
                <input id="on" type="submit" value="Lights ON">
            </form>
            
            <form method="post" action="web_controls.cgi">
                <input type="hidden" name="message" value="Off"/>
                <input id="off" type="submit" value="Lights OFF">
            </form>

""")

if message:
    if message == "On":
        os.system('pkill -f "bash $SYNCHRONIZED_LIGHTS_HOME/bin"')
        os.system('pkill -f "python $SYNCHRONIZED_LIGHTS_HOME/py"')
        os.system("python ${SYNCHRONIZED_LIGHTS_HOME}/py/hardware_controller.py --state=on")
        logger.info("Turned on lights")
    if message == "Off":
        os.system('pkill -f "bash $SYNCHRONIZED_LIGHTS_HOME/bin"')
        os.system('pkill -f "python $SYNCHRONIZED_LIGHTS_HOME/py"')
        os.system("python ${SYNCHRONIZED_LIGHTS_HOME}/py/hardware_controller.py --state=off")
        logger.info("Turned off lights")
    if message == "Next":
        os.system('pkill -f "python $SYNCHRONIZED_LIGHTS_HOME/py"')
        sleep(.1)
    if message == "Speakers On":
        connection = connect()
        if connection:
            send_commands.send_command_server(connection, "Speakers", "on", confirm=False)
            logger.info("Sent command to turn on speakers")

        #os.system("python ${BROADLINK}/send_commands.py --on Speakers")
        #os.system("echo 'broadlink: ${BROADLINK}'")
        sleep(.1)
    if message == "Speakers Off":
        connection = connect()
        if connection:
            send_commands.send_command_server(connection, "Speakers", "off", confirm=False)
            logger.info("Sent command to turn off speakers")

        #os.system('python ${BROADLINK}/send_commands.py --off Speakers')
        sleep(.1)
    if message == "System Off":
        connection = connect()
        if connection:
            #os.system('python ${BROADLINK}/send_commands.py --off Speakers')
            send_commands.send_command_server(connection, "Speakers", "off", confirm=False)
            logger.info("Sent command to turn off system")
        os.system('pkill -f "bash $SYNCHRONIZED_LIGHTS_HOME/bin"')
        os.system('pkill -f "python $SYNCHRONIZED_LIGHTS_HOME/py"')
        os.system("python ${SYNCHRONIZED_LIGHTS_HOME}/py/hardware_controller.py --state=off")
        sleep(.1)

    if message == "Start":
        connection = connect()
        if connection:
            send_commands.send_command_server(connection, "Speakers", "on", confirm=False)
            logger.info("Sent command to turn on speakers (part of Start)")
        os.system('pkill -f "bash $SYNCHRONIZED_LIGHTS_HOME/bin"')
        os.system('pkill -f "python $SYNCHRONIZED_LIGHTS_HOME/py"')
        os.system("${SYNCHRONIZED_LIGHTS_HOME}/bin/play_sms &")
        os.system("${SYNCHRONIZED_LIGHTS_HOME}/bin/check_sms &")
        sleep(.1)

    if message == "Restart Server":
        import shlex
        from subprocess import Popen
        stop=f"{HOME}/bin/stop_microweb"
        start=f"{HOME}/bin/start_microweb"

        #c = f'nohup {stop} && sleep 2 && {start} >> $SYNCHRONIZED_LIGHTS_HOME/logs/microweb.log 2>&1 &'
        c = f'sleep 0 && {stop} && sleep 2 && {start} >> $SYNCHRONIZED_LIGHTS_HOME/logs/microweb.log 2>&1'
        cmds = shlex.split(c)

        p = Popen(cmds, start_new_session=True)
        p.send_signal(signal.SIGSTOP)

        #Popen(c, stdout=devnull, stderr=devnull, shell=True)

cmd = 'pgrep -f "python $SYNCHRONIZED_LIGHTS_HOME/py/synchronized_lights.py"'
if os.system(cmd) == 0:
    print("""
        <form method="post" action="web_controls.cgi">
            <input type="hidden" name="message" value="Next"/>
            <input id="next" type="submit" value="Play Next">
        </form>
""")
else:
    print("""
        <form method="post" action="web_controls.cgi">
            <input type="hidden" name="message" value="Start"/>
            <input id="start" type="submit" value="START">
        </form>
""")

## Speakers
print("""
            <form method="post" action="web_controls.cgi">
                <input type="hidden" name="message" value="Speakers On"/>
                <input id="speakers_on" type="submit" value="Speakers ON">
            </form>

             <form method="post" action="web_controls.cgi">
                <input type="hidden" name="message" value="Speakers Off"/>
                <input id="speakers_off" type="submit" value="Speakers OFF">
            </form>

        <form method="post" action="web_controls.cgi">
            <input type="hidden" name="message" value="System Off"/>
            <input id="system_off" type="submit" value="OFF">
        </form>

        <form method="post" action="web_controls.cgi">
            <input type="hidden" name="message" value="Restart Server"/>
            <input id="restart" type="submit" value="Restart Server">
        </form>
""")

if message:
    print("""<h2>Executed command: %s</h2>""" % html.escape(message))


# Print log

def tail(filename, n=10):
    'Return the last n lines of a file'
    with open(filename) as f:
        return deque(f, n)

log = f"{os.environ['SYNCHRONIZED_LIGHTS_HOME']}/logs/microweb.log"
#log = logging.getLoggerClass().root.handlers[0].baseFilename
if Path(log).exists():
    #print(log)
    print('<p class="log">')
    print("<br>".join(tail(log,15)).replace(' ', '&nbsp;'))
    print('</p>')
print("</body></html>")

