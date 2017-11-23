#!/usr/bin/env python3
#This codes is intended to create class of functions that readthe MPC3008 ADC chip and convert to engineering units.
#MFRIED 01/04/2015 This now works - however to avoid /dev/mem access error this must be started using sudo python3 filename command.
#Or - just start a root based idle3 window using sudo idle3 command.
# this file could not be imported when the name started with 3008


import time
import os
import RPi.GPIO as GPIO\
#Must have space here. Why???
GPIO.setmode(GPIO.BCM)
DEBUG = 1


class mpc3008_adc:
        def __init__(self,adcnum, clockpin, mosipin, misopin, cspin):
                self.adcnum=adcnum
                self.clockpin = clockpin
                self.mosipin = mosipin
                self.misopin = misopin
                self.cspin = cspin
        
        def gpio_setup(self):
                # set up the SPI interface pins - needs to be called only once.
                #print('Setting Up GPIO!')
                GPIO.setwarnings(False)
                GPIO.setup(self.mosipin, GPIO.OUT)
                GPIO.setup(self.misopin, GPIO.IN)
                GPIO.setup(self.clockpin, GPIO.OUT)
                GPIO.setup(self.cspin, GPIO.OUT)
        

        # read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
        def readadc(self):#, adcnum, clockpin, mosipin, misopin, cspin):
                if ((self.adcnum > 7) or (self.adcnum < 0)):
                        return -1
                GPIO.output(self.cspin, True)

                GPIO.output(self.clockpin, False)  # start clock low
                GPIO.output(self.cspin, False)     # bring CS low

                commandout = self.adcnum
                commandout |= 0x18  # start bit + single-ended bit
                commandout <<= 3    # we only need to send 5 bits here
                for i in range(5):
                        if (commandout & 0x80):
                                GPIO.output(self.mosipin, True)
                        else:
                                GPIO.output(self.mosipin, False)
                        commandout <<= 1
                        GPIO.output(self.clockpin, True)
                        GPIO.output(self.clockpin, False)

                adcout = 0
                # read in one empty bit, one null bit and 10 ADC bits
                for i in range(12):
                        GPIO.output(self.clockpin, True)
                        GPIO.output(self.clockpin, False)
                        adcout <<= 1
                        if (GPIO.input(self.misopin)):
                                adcout |= 0x1

                GPIO.output(self.cspin, True)
        
                adcout >>= 1       # first bit is 'null' so drop it
                return adcout

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler

