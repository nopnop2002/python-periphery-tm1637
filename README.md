# python-periphery-tm1637
[![CodeFactor](https://www.codefactor.io/repository/github/magnetrwn/python-periphery-tm1637/badge)](https://www.codefactor.io/repository/github/magnetrwn/python-periphery-tm1637)

<b>This module contains functions to drive the TM1637 display module as well as clock, scrolling ASCII text and system information functionality. Attaching this to a SBC can give useful insight on the system status or just keep time.</b>

TM1637 8 segment, 4 digit LED examples:
<p float:"left">
  <img src="https://user-images.githubusercontent.com/6020549/90970987-5b45e480-e546-11ea-854b-c11eaf146ac8.JPG" title="TM1637-White" width="40%"/>
  <img src="https://user-images.githubusercontent.com/6020549/90970988-5e40d500-e546-11ea-84bf-55ff035998f3.JPG" title="TM1637-Red" width="40%"/>
</p>

# Hardware requiments
TM1637 8 segment 0.36INCH Digital Display Tube 4 digit LED module:
<p float:"left">
  <img src="https://user-images.githubusercontent.com/6020549/90970978-52551300-e546-11ea-9764-4527ce3c6a49.JPG" title="TM1637-1" width="40%"/>
  <img src="https://user-images.githubusercontent.com/6020549/90970981-5719c700-e546-11ea-8e48-ac4c0d7b5dc6.JPG" title="TM1637-2" width="40%"/>
</p>

# Software requiments
Please install the "python-periphery" library.

```
sudo apt update
sudo apt install git python3-pip python3-setuptools
git clone https://github.com/vsergeev/python-periphery.git
cd python-periphery/
python3 -m pip install python-periphery
```

# Wiring
|LED Module|Raspberry Pi|
|:-:|:-:|
|CLK|Pin#5|
|DIO|Pin#3|
|GND|GND|
|5V or 3V3|3V3|

(Use the next table if you are not running this on a Raspberry Pi)

# Setup
```
git clone https://github.com/nopnop2002/python-periphery-tm1637
cd python-periphery-tm1637/
vi tm1637.py
```
If you use this module on something other than Raspberry Pi, you should change the following:
```
_DEF_TM1637_CLK = ##           # Default GPIO for CLK
_DEF_TM1637_DIO = ##           # Default GPIO for DIO
```
These default names are loaded as implicit parameters on creation of an instance of TM1637, but other values can be passed as well to manage multiple displays at once. In that case also make sure to export all GPIO pins used as "out" before creation (see the first lines of the \_\_main\_\_).

||CLK|DIO|
|:-:|:-:|:-:|
|Raspberry Pi|3|2|
|Orange Pi Allwinner H2+|11|12|
|Orange Pi Allwinner H3|11|12|
|Orange Pi Allwinner H5|11|12|
|Orange Pi Allwinner A64|226|227|
|Orange Pi 3|121|122|
|Orange Pi Lite2|229|230|
|Orange Pi OnePlus|229|230|
|Orange Pi RK3399|44|43|
|Orange Pi 4|65|64|

Other default values can be set for more parameters as well.
```
_DEF_TM1637_BRIGHT = 0xA       # Default brightness from 0x0 to 0xF
_DEF_TM1637_ANIM_DELAY = 0.2   # Default animation delay in seconds
```
# Start demo
```
python3 tm1637.py
```
Privilege elevation might be required.
```
sudo -E python3 tm1637.py
```
