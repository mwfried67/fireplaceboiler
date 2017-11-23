# fireplaceboiler
PI based fireplace boiler controller software development
171112 Moving to Rasberry Pi3!!*****************************88
Copied marcus_py and tried to run boilercontrol_9.py. Ran fine on RPi1. I get this error in thonny:
Traceback (most recent call last):
  File "/home/pi/Documents/marcus_py/boiler_control_p2/boilercontrol_v9.py", line 9, in <module>
    from Tkinter import *
ImportError: No module named 'Tkinter'



Tried:
sudo apt-get install python-tk - already there no update
sudo pip install RPi.GPIO b- Already Satisfied
sudo apt-get update - Seemed to do somethhing but still get same error.
sudo apt-get install build-essential python-dev python-pip python-smbus git - did something but did not fix error.
sudo pip install RPi.GPIO

Problem is Thonny is running python 3. Not python2. In python3 Tkinter becomes tkinter. ... Solution is to run python2. Need to figure out how to do
this in Thonny. Thonny only runs python 3.4 and later.

Need this.
cd ~
git clone https://github.com/adafruit/Adafruit_Python_MAX31855.git
cd Adafruit_Python_MAX31855
sudo python setup.py install

boilercontrol_9.py works now using idle!! On RPi3!! Yay. Much faster...

***********************************************************************************
01/04/2015
Notes on getting python script to run on startup:


This website desribes how to get a script to run using crontab
http://www.instructables.com/id/Raspberry-Pi-Launch-Python-script-on-startup/

created boilercontrol.sh file and made executable with "chmod 755 boilercontrol.sh" 
checked execution of this file with "sh boilercontrol.sh". Placed in the /home/pi/.config/autostart directory.

edited crontab with "crontab -e" command.
note that "sudo crontab -e" edits a different crontab.
"crontab -l" list contab file.

Added line to crontab -e shown below:
@reboot sh /home/pi/.config/autostart/boilercontrol.sh >/home/pi/logs/cronlog 2>&1


tried adding to sudo and non-sudo crontab. Niether worked.
Checked error log as follows

go to home/pi/logs directory and type cat cronlog. Other option is to look at log in leafpad.

Got it to execute the boilercontrol.sh file and attempt to start boilercontol_v2 file but there was 
a error indicated in cronlog as shown below:

Traceback (most recent call last):
  File "boilercontrol_v2.py", line 123, in <module>
    root=tk.Tk()
  File "/usr/lib/python3.2/tkinter/__init__.py", line 1701, in __init__
    self.tk = _tkinter.create(screenName, baseName, className, interactive, wantobjects, useTk, sync, use)
_tkinter.TclError: no display name and no $DISPLAY environment variable


I suspect that somehow crontab is executed before evertything is loaded and this error results.

I will come back to this issue later. 

Update- Tried adding these lines to etc/init.d/rc.local file and it did not work. (www.rasberrypi.org -look up rc.local)

python3 /home/pi/marcus_py/boilercontrol_v2.py $

exit 0



Got 3008_ADC_V2.py working today. This is a class module that reads MPC3008 ADC chip SPI. Next step here is to add the
conversion to engineering units.

01/11/2015
Finally got boilercontrol.py to fire up on bootup.Charlie Snyder figured it out for me. Key is that it has to be
started after x-term is started. Charlie tells me that the scripts in /home/pi/.config/autostart get run after 
xterm is started. These scripts must be of the right format to run. Here is the marcus.desktop exectable file 
that got it started:

[Desktop Entry]
Name=Marcus
Exec=python3 /home/pi/marcus_py/boilercontrol_v2.py
Type=application
StartupNotify=false

The other key was a hashbang line in the boilercontrol_v2.py itself as follows:

#!/usr/bin/python3

This line tells it to use the python3 interpreter. Now one can simply type the name this file in lxterm and it will
run it without typing python before it.


The 2nd way to get it to run:


Here is the file

/etc/xdg/lxsession/LXDE/autostart

And the web site describing it

http://www.raspberrypi.org/forums/viewtopic.php?f=31&t=43509


Here is what was in the file:
@lxpanel --profile LXDE
@pcmanfm --desktop --profile LXDE
@xscreensaver -no-splash
@/home/pi/marcus_py/boilercontrol_v2.py

I am going to stick with the first way.

***********************************
150314 plotpy installed.
sudo pip install plotpy
this plots a streaming file to the web. 
Search for raspberry Pi + TMP36 Temperature

Thought about it for a bit - decided I wanted self contained ploting capability.

Going to try gnuplot
sudo apt-get install gnuplot-X11
http://www.raspberrypi-spy.co.uk/2014/04/how-to-use-gnuplot-to-graph-data-on-the-raspberry-pi/
Problem with gnuplot is that I cannot figure out how to run via python. Cannot find script example.

So - I will try matplotlib which works via python.

Installed as follows: (pi3.sites.sheffield.ac.uk/tutorials/set-up-your-pi)
sudo apt-get install python-scipy
sudo apt-get install python-matplotlib

Got matplotlib to plot a file. left of at plotfile2.py 
************************************
150329
Got FIFO datafile script working that saves time and data to file of fixed total lines. When it fills up it delete's
the oldest line and saves the latest. file_2.py

Got matplotlib script working that plots a dataset with an X axis of time. File plotfile3.py.
Included figuring out how to save current time to a file.

Next step is to transform these to class modules and run them via the main boilercontrol script.

file_3.py is now a class module. Still need to make plotfile3.py a class module.

Notices that there is a lot of noise on TC and on pots. Need noise suppression.
**************************************************
150405
Converted plotfile3 to class plotfile4. This does not work as it takes wayyyy tooo looong to generate a new plot
every time. Need a new approach. Looking into matplotlib animation.

boilercontrol_11.py calls both plotfile4 and file_3.py files. Added signal processing to TC input. Now backing up on
memory stick.


