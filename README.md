# python-periphery-tm1637
[![CodeFactor](https://www.codefactor.io/repository/github/magnetrwn/python-periphery-tm1637/badge)](https://www.codefactor.io/repository/github/magnetrwn/python-periphery-tm1637)

<b>This module contains methods to drive the TM1637 display module as well as clock, scrolling ASCII text and system information functionality. Attaching this to a SBC can give useful insight on the system status or just keep time.</b>

TM1637 8 segment, 4 digit LED examples:
<p float:"left">
  <img src="https://user-images.githubusercontent.com/94263372/213289698-4f7dbbc6-cced-477f-9ff1-f922cb8bec58.gif" title="TM1637-Red-Clock"/>
  <!--img src="https://user-images.githubusercontent.com/6020549/90970987-5b45e480-e546-11ea-854b-c11eaf146ac8.JPG" title="TM1637-White" width="40%"/-->
  <img src="https://user-images.githubusercontent.com/6020549/90970988-5e40d500-e546-11ea-84bf-55ff035998f3.JPG" title="TM1637-Red" width="35.556%"/>
</p>

# Hardware requiments
TM1637 8 segment 0.36INCH Digital Display Tube 4 digit LED module:
<p float:"left">
  <img src="https://user-images.githubusercontent.com/6020549/90970978-52551300-e546-11ea-9764-4527ce3c6a49.JPG" title="TM1637-1" width="43%"/>
  <img src="https://user-images.githubusercontent.com/6020549/90970981-5719c700-e546-11ea-8e48-ac4c0d7b5dc6.JPG" title="TM1637-2" width="43%"/>
</p>

# Software requiments
python-periphery library.

```
sudo apt update
sudo apt install git python3-pip python3-setuptools
git clone https://github.com/vsergeev/python-periphery.git
cd python-periphery/
python3 -m pip install python-periphery
```

# Why python-periphery   
python-periphery is a highly compatible library.   
Available for most Pi boards.   

# Wiring
|LED Module|Raspberry Pi||
|:-:|:-:|:-:|
|CLK|Pin#5|(*1)|
|DIO|Pin#3|(*1)|
|GND|GND||
|5V|3V3|(*2)|

(*1)   
You can use any GPIO you like in the startup arguments.   

(*2)   
RPi reads data from DIO, so it must be 3V3.   

# Setup
```
cd $HOME
git clone https://github.com/nopnop2002/python-periphery-tm1637
cd python-periphery-tm1637/
python3 tm1637.py
```
If you use this module on something other than Raspberry Pi, you will need to change the GPIO.   
```
$ python3 tm1637.py --help
usage: tm1637.py [-h] [--clk CLK] [--dio DIO] [--text TEXT]

optional arguments:
  -h, --help   show this help message and exit
  --clk CLK    CLK GPIO
  --dio DIO    DIO GPIO
  --text TEXT
```

If you use Pin#3 and Pin#5, it will be as follows.   

||CLK(Pin#5)|DIO(Pn#3)||
|:-:|:-:|:-:|:-:|
|Raspberry Pi|3|2|Default|
|Orange Pi Allwinner H2+|11|12||
|Orange Pi Allwinner H3|11|12||
|Orange Pi Allwinner H5|11|12||
|Orange Pi Allwinner A64|226|227||
|Orange Pi 3|121|122||
|Orange Pi Lite2|229|230||
|Orange Pi OnePlus|229|230||
|Orange Pi RK3399|44|43||
|Orange Pi 4|65|64||

Other default values can be set for more parameters as well.
```
_DEF_TM1637_BRIGHT = 0xA       # Default brightness from 0x0 to 0xF
_DEF_TM1637_ANIM_DELAY = 0.2   # Default animation delay in seconds
```
Remember to change your CPU temperature sensor in the script if necessary, inside \_demo():
```
show_on_high_cpu_thermal(tm, 50, "/sys/devices/virtual/thermal/thermal_zone0/temp")
# Please change your cpu sensor path if different
```
# Start Auto Demo
```
python3 tm1637.py
```
Privilege elevation might be required.
```
sudo -E python3 tm1637.py
```

# Display text
```
python3 tm1637.py --text="any_text"
```
Privilege elevation might be required.
```
sudo -E python3 tm1637.py --text="any_text"
```
