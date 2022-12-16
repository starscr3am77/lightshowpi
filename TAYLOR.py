import shlex
import os
import signal
HOME = os.environ["SYNCHRONIZED_LIGHTS_HOME"]
stop=f"{HOME}/bin/stop_microweb"
start=f"{HOME}/bin/start_microweb"

c = f'nohup {stop} && sleep 2 && {start} >> $SYNCHRONIZED_LIGHTS_HOME/logs/microweb.log 2>&1 &'
c = f'{stop} && sleep 2 && {start} >> $SYNCHRONIZED_LIGHTS_HOME/logs/microweb.log 2>&1'
cmds = shlex.split(c)

if True:
    from subprocess import Popen
    import shlex
    devnull = open(os.devnull, 'wb') # Use this in Python < 3.3
    p = Popen(cmds, start_new_session=True, close_fds=False)
    #p.detach()
    p.send_signal(signal.SIGSTOP)
#Popen(c, stdout=devnull, stderr=devnull, shell=True)

else:
    import multiprocessing
    import subprocess

    def command():
        subprocess.Popen(cmds)

    multiprocessing.Process(command)
    p.daemon = True
    p.start()
