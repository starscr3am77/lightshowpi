import threading
import os, sys
import logging
import socket
broadlink = os.getenv("BROADLINK")
# Needed for relay.py
sys.path.append(broadlink)
import relay as relay_package

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

def create_relay():
    ## START INTERNAL RELAY SERVER
    logger.info("Starting relay...")

    try:
        destination_address = "192.168.187.103"
        destination_port = 32001

        try:
            s = socket.socket()
            is_remote = s.connect_ex((destination_address, destination_port))
        finally:
            s.close()
    except Exception as e:
        logger.error(str(e))
        is_remote=True
    finally:
        if is_remote:
            destination_address = "fife.entrydns.org"
            destination_port = 57325
            logger.info("Using remote WAN address for Broadlink")
        else:
            logger.info("Connected to Broadlink using LAN")

    relay = threading.Thread(target=relay_package.TheServer,
                              kwargs={"local_host":"",
                                      "local_port":39554,
                                      "destination_address":destination_address,
                                      "destination_port":destination_port,
                                      "autostart":True},
                              ).start()

if __name__=='__main__':
    create_relay()
