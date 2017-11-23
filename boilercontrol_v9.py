#!/usr/bin/env python
#Python 2.7 - moved to 2.7 because adafruit max38155 software did not exist for python 3.
#This version works. Archived as after_V5 1/03/2015 mfried
#Now moving on to boilercontrol_vx nomenclature.
#

from ADC_3008_V4 import * #Note - cannot start file name with 3008 for some reason.
from td_lookup_2 import *
from Tkinter import *
import Tkinter as tk
import tkFont
import time

#****Start Adafruit MAX31855 SPI Thermocouple module setup code**********
#import Adafruit_GPIO.SPI as SPI # does not appear to be needed.
import Adafruit_MAX31855.MAX31855 as MAX31855

# Raspberry Pi software SPI configuration.
CLK = 22
CS  = 27
DO  = 17
sensor = MAX31855.MAX31855(CLK, CS, DO)
#****End  Adafruit MAX31855 SPI Thermocouple module setup code**********

#***Start set up for MPC3008 ADC Concverter chip on SPI******************
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25
    
#Set up ADC's
#Water in Temperature
adc_rd0 = mpc3008_adc(0,SPICLK, SPIMOSI, SPIMISO, SPICS)
adc_rd0.gpio_setup()  #need only do once.
#Water out temperature
adc_rd1 = mpc3008_adc(1,SPICLK, SPIMOSI, SPIMISO, SPICS)
#Room Temp
adc_rd2 = mpc3008_adc(2,SPICLK, SPIMOSI, SPIMISO, SPICS)
#Room Temp setpoint
adc_rd3 = mpc3008_adc(3,SPICLK, SPIMOSI, SPIMISO, SPICS)

#Set up thermistor voltage to temperature tranfer fucntion.
#This is for a Mouser 527-0503-10k with 5V V+ and 5K pulldown.
myarray = [[0.2419, 0.3175, 0.4112, 0.5254, 0.6619, 0.8207, 1.0028, 1.2059, 1.4285, 1.6666, 1.9149, 2.1686, 2.4217, 2.6695, 2.9073, \
           3.1316, 3.3395, 3.530, 3.7026, 3.8568, 3.9948, 4.1165, 4.2237, 4.3178, 4.4001, 4.4717, 4.5344, 4.5889, 4.6365], \
          [-4, 5, 14, 23, 32, 41, 50, 59, 68, 77, 86, 95, 104, 113, 122, 131, 140, 149, 158, 167, 176, 185, 194, 203, 212, 221, 230, 239, 248]]
        

v_to_degF = td_lookup(myarray)

flue_t = 451
water_t = 243
room_t = 68.1
room_t_sp = 70.1
fan_status  = 'off'
pump_status = 'on'



def Draw(): #This draws the control interface display
    global flue_t_f # Frame variable names.
    global pump_s_f
    global fan_s_f
    global water_in_t_f
    global water_out_t_f
    global boiler_rise_t_f
    global room_t_f
    global room_t_sp_f
    customFont = tkFont.Font(family="Helvetica", size=18, weight="bold")#Works!!
    #***************Column #0*******************************
    frame0=tk.Frame(root,width=200,height=200,relief='solid',bd=1) #Note that the width and height here do not seem to have an effect.
    frame0.place(x=10,y=10)
    #text=tk.Label(frame0,text='Flue Temp(Deg F)',font=16) # This works.
    #text=tk.Label(frame0,text='Flue Temp(Deg F)',font="-weight bold") # This works too.
    text=tk.Label(frame0,text='Flue Temp(Deg F)  ',font=customFont) # Yes!! Now this works! This is the way to go.
    text.pack()
    flue_t_f=tk.Label(frame0,text='Dummy',font=customFont)
    flue_t_f.pack()

    frame1=tk.Frame(root,width=100,height=100,relief='solid',bd=1)
    frame1.place(x=10,y=100)
    text=tk.Label(frame1,text='  Pump Status       ',font=customFont)
    text.pack()
    pump_s_f=tk.Label(frame1,text='ON',font=customFont)
    pump_s_f.pack()

    frame2=tk.Frame(root,width=100,height=100,relief='solid',bd=1)
    frame2.place(x=10,y=200)
    text=tk.Label(frame2,text='    Fan Status        ',font=customFont)
    text.pack()
    fan_s_f=tk.Label(frame2,text='OFF',font=customFont)
    fan_s_f.pack()
    #***************Column #1*******************************
    frame3=tk.Frame(root,width=100,height=100,relief='solid',bd=1)
    frame3.place(x=250,y=10)
    text=tk.Label(frame3,text=' Boiler In(Deg F)  ',font=customFont)
    text.pack()
    water_in_t_f=tk.Label(frame3,text='Dummy',font=customFont)
    water_in_t_f.pack()

    frame4=tk.Frame(root,width=100,height=100,relief='solid',bd=1)
    frame4.place(x=250,y=100)
    text=tk.Label(frame4,text=' Boiler Out(Deg F) ',font=customFont)
    text.pack()
    water_out_t_f=tk.Label(frame4,text='Dummy',font=customFont)
    water_out_t_f.pack()

    frame5=tk.Frame(root,width=100,height=100,relief='solid',bd=1)
    frame5.place(x=250,y=200)
    text=tk.Label(frame5,text=' Boiler Rise(Deg F)',font=customFont)
    text.pack()
    boiler_rise_t_f=tk.Label(frame5,text='Dummy',font=customFont)
    boiler_rise_t_f.pack()

    #***************Column #2*******************************
    frame6=tk.Frame(root,width=100,height=100,relief='solid',bd=1)
    frame6.place(x=500,y=10)
    text=tk.Label(frame6,text='   Room Temp(Deg F)             ',font=customFont)
    text.pack()
    room_t_f=tk.Label(frame6,text='70',font=customFont)
    room_t_f.pack()

    frame7=tk.Frame(root,width=100,height=100,relief='solid',bd=1)
    frame7.place(x=500,y=100)
    text=tk.Label(frame7,text='Room Temp Setpoint(Deg F) ',font=customFont)
    text.pack()
    room_t_sp_f=tk.Label(frame7,text='Dummy',font=customFont)
    room_t_sp_f.pack()


def Refresher():
    global flue_t
    global water_in_t
    global water_out_t
    global room_t
    global room_t_sp
    global pump_s
    global fan_s
    global boiler_rise_t


    # Read temperatures
    update_temp()

    # Perform control of hardware.
    # control()

    #Record Data
    #RecordData()

    #textx.configure(text=time.asctime())#This displays time in text

    #Change GUI temperature readings.

    
    water_in_t_f.configure(text='%3.0f'%water_in_t)
    water_out_t_f.configure(text='%3.0f'%water_out_t)
    room_t_f.configure(text='%3.0f'%room_t)
    room_t_sp_f.configure(text='%3.0f'%room_t_sp)
    flue_t_f.configure(text='%3.0f'%flue_t)
    #Run this sub periodically.
    root.after(100, Refresher) # every second...


def update_temp(): # This Now Works!!!!!!!!
    global flue_t
    global water_in_t
    global water_out_t
    global room_t
    global room_t_sp
    global pump_s
    global fan_s
    global boiler_rise_t
    
    water_in_t = adc_rd0.readadc()*3.3/1024
    water_in_t = v_to_degF.td_lu(water_in_t)
    
    water_out_t = adc_rd1.readadc()*3.3/1024
    water_out_t = v_to_degF.td_lu(water_out_t)

    room_t = adc_rd2.readadc()*3.3/1024
    room_t = v_to_degF.td_lu(room_t)

    room_t_sp = adc_rd3.readadc()*3.3/1024
    room_t_sp = v_to_degF.td_lu(room_t_sp)

    flue_t = sensor.readTempC()*1.8+32
    
    #internal = sensor.readInternalC()
root=tk.Tk()
root.geometry("900x500+0+0")
root.wm_title('Fireplace Status2')
Draw()
Refresher()
root.mainloop()





