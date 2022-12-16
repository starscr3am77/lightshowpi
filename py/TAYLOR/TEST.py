#!/usr/bin/env python

import alsaaudio as aa

if False:
    import hardware_controller

    hc = hardware_controller.Hardware(param_config=args.config)

    # get copy of configuration manager
    cm = hc.cm

output_device = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL, 'default',
                       #cm.lightshow.audio_out_card,
                       channels=1,
                       rate=48000,
                       format=aa.PCM_FORMAT_S16_LE,
                       periodsize=2048)

streaming = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NORMAL, 'default',
                        channels=1)
                        #rate=48000,
                        #format=aa.PCM_FORMAT_S16_LE,
                        #periodsize=2048)
def test():
    import wiringpi
    import time
    #from RF24 import *

    PIN_CE = 0  # (physical pin 11) Chip Enable pin for RF24
    PIN_CS = 10 # (physical pin 24) Chip Select pin for RS24
    PIN_PAIRLED = 5 # (physical pin 18)

    wiringpi.wiringPiSetup()
    wiringpi.pinMode(PIN_PAIRLED, 1)

    wiringpi.digitalWrite(PIN_PAIRLED, 1)
    time.sleep(1)
    wiringpi.digitalWrite(PIN_PAIRLED, 0)

    radio = RF24(PIN_CE, PIN_CS);
    radio.begin()
