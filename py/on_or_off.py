#!/usr/bin/env python

import argparse
import Platform
import configuration_manager

# Test if running on a RaspberryPi
is_a_raspberryPI = Platform.platform_detect() == 1

if is_a_raspberryPI:
    import wiringpipy as wiringpi
else:
    import wiring_pi as wiringpi

class Hardware:
    def __init__(self, param_config=None):
        self.cm = configuration_manager.Configuration(param_config=param_config)
        self.initialize()

    def initialize(self):
        """Set pins as outputs and initialize wiringPi."""
        wiringpi.wiringPiSetupPY()
        for pin in self.cm.hardware.gpio_pins:
            wiringpi.pinModePY(pin, 1)  # Set as output

    def set_all_lights(self, state):
        """Set all lights to either on or off."""
        # Calculate the output value based on active_low_mode
        output = 0 if self.cm.hardware.active_low_mode == state else 1
        
        # Set all pins at once
        for pin in self.cm.hardware.gpio_pins:
            wiringpi.digitalWritePY(pin, output)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--state', choices=["off", "on"], required=True,
                      help='turn off or on')
    parser.add_argument('--config', default="",
                      help='Config File Override')
    args = parser.parse_args()

    # Initialize hardware
    hc = Hardware(param_config=args.config)
    
    # Set lights based on state
    hc.set_all_lights(args.state == "on")

if __name__ == "__main__":
    main()
