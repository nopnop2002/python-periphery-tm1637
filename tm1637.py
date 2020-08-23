'''
python-periphery TM1637 4Digits 8Segment LCD example

I ported from here
https://github.com/johnlr/raspberrypi-tm1637

'''
#!/usr/bin/python
#-*- encoding: utf-8 -*-

import subprocess
from time import time, sleep, localtime

from periphery import GPIO

CLK = 3
DIO = 2

"""
      A
     ---
  F |   | B
     -G-
  E |   | C
     ---
      D

"""


class TM1637:
    I2C_COMM1 = 0x40
    I2C_COMM2 = 0xC0
    I2C_COMM3 = 0x80
    digit_to_segment = [
        0b0111111, # 0
        0b0000110, # 1
        0b1011011, # 2
        0b1001111, # 3
        0b1100110, # 4
        0b1101101, # 5
        0b1111101, # 6
        0b0000111, # 7
        0b1111111, # 8
        0b1101111, # 9
        0b1110111, # A
        0b1111100, # b
        0b0111001, # C
        0b1011110, # d
        0b1111001, # E
        0b1110001  # F
        ]

    def __init__(self, clk, dio):
        self.clk = clk
        self.dio = dio
        self.brightness = 0x0f

        self.gpio_clk = GPIO(self.clk, "out")
        self.gpio_dio = GPIO(self.dio, "out")

    def bit_delay(self):
        sleep(0.001)
        return
   
    def set_segments(self, segments, pos=0):
        # Write COMM1
        self.start()
        self.write_byte(self.I2C_COMM1)
        self.stop()

        # Write COMM2 + first digit address
        self.start()
        self.write_byte(self.I2C_COMM2 + pos)

        for seg in segments:
            self.write_byte(seg)
        self.stop()

        # Write COMM3 + brightness
        self.start()
        self.write_byte(self.I2C_COMM3 + self.brightness)
        self.stop()

    def start(self):
        self.gpio_clk.write(True)
        self.gpio_dio.write(True)
        self.gpio_dio.write(False)
        self.gpio_clk.write(False)
   
    def stop(self):
        self.gpio_clk.write(False)
        self.gpio_dio.write(False)
        self.gpio_clk.write(True)
        self.gpio_dio.write(True)
  
    def write_byte(self, data):
        #print("data={:x}".format(data))
        for i in range(8):
            self.gpio_clk.write(False)
            if data & 0x01:
                self.gpio_dio.write(True)
            else:
                self.gpio_dio.write(False)
            data >>= 1
            self.gpio_clk.write(True)

        self.gpio_clk.write(False)
        self.gpio_dio.write(True)
        self.gpio_clk.write(True)
        self.gpio_dio = GPIO(self.dio, "in")

        while self.gpio_dio.read():
            sleep(0.001)
            if self.gpio_dio.read():
                self.gpio_dio = GPIO(self.dio, "out")
                self.gpio_dio.write(False)
                self.gpio_dio = GPIO(self.dio, "in")
        self.gpio_dio = GPIO(self.dio, "out")


def show_ip_address(tm):
    #ipaddr = subprocess.check_output("hostname -I", shell=True, timeout=1).strip().split(b".")
    #ipaddr = subprocess.check_output("hostname -I", shell=True).strip().split(b".")
    ipaddr = subprocess.check_output("hostname -I", shell=True).strip()
    ipaddr = ipaddr.split(" ")
    ipaddr = ipaddr[0].split(".")
    for octet in ipaddr:
        tm.set_segments([0, 0, 0, 0])
        sleep(0.1)
        tm.set_segments([tm.digit_to_segment[int(x) & 0xf] for x in octet])
        sleep(0.9)


def show_clock(tm):
        t = localtime()
        sleep(1 - time() % 1)
        d0 = tm.digit_to_segment[t.tm_hour // 10] if t.tm_hour // 10 else 0
        d1 = tm.digit_to_segment[t.tm_hour % 10]
        d2 = tm.digit_to_segment[t.tm_min // 10]
        d3 = tm.digit_to_segment[t.tm_min % 10]
        tm.set_segments([d0, 0x80 + d1, d2, d3])
        sleep(.5)
        tm.set_segments([d0, d1, d2, d3])

if __name__ == "__main__":
    gpio_clk = GPIO(CLK, "out")
    gpio_dio = GPIO(DIO, "out")

    tm = TM1637(CLK, DIO)

    show_ip_address(tm)

    try:
        while True:
            show_clock(tm)
    except KeyboardInterrupt:
        pass

    print('cleanup')
    gpio_clk.close()
    gpio_dio.close()
