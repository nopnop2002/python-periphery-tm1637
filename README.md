# python-periphery-tm1637
python-periphery TM1637 8-Segment 4-Digits LED example

![TM1637-White](https://user-images.githubusercontent.com/6020549/90970987-5b45e480-e546-11ea-854b-c11eaf146ac8.JPG)

![TM1637-Red](https://user-images.githubusercontent.com/6020549/90970988-5e40d500-e546-11ea-84bf-55ff035998f3.JPG)

# Hardware requiment
TM1637 8-Segments 0.36INCH Digital Display Tube 4-Digit LED Module.   
![TM1637-1](https://user-images.githubusercontent.com/6020549/90970978-52551300-e546-11ea-9764-4527ce3c6a49.JPG)

![TM1637-2](https://user-images.githubusercontent.com/6020549/90970981-5719c700-e546-11ea-8e48-ac4c0d7b5dc6.JPG)

# Software requiment
python-periphery library.   

```
sudo apt update
sudo apt install git python3-pip python3-setuptools
git clone https://github.com/vsergeev/python-periphery.git
cd python-periphery/
python3 -m pip install python-periphery
```

# Wireing
|LED Module|---|Raspberry Pi|
|:-:|:-:|:-:|
|CLK|---|Pin#5|
|DIO|---|Pin#3|
|GND|---|GND|
|5V|---|3V3|

# Setup
```
git clone https://github.com/nopnop2002/python-periphery-tm1637
cd python-periphery-tm1637/
vi tm1637.py
```

You have to change this line.   
```
CLK = 3
DIO = 2
```

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

# Start demo
```
sudo python ./tm1637.py
```
