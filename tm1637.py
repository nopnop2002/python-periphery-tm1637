'''
python-periphery TM1637 4Digits 8Segment LCD example

I ported from here
https://github.com/johnlr/raspberrypi-tm1637

'''

#!/usr/bin/python3
#-*- encoding: utf-8 -*-

import subprocess
from time import time, sleep, localtime

from periphery import GPIO

CLK        = 11    # GPIO for CLK
DIO        = 12    # GPIO for DIO
BRIGHT     = 0xA   # from 0x0 to 0xF
ANIM_DELAY = 0.375 # animation delay in seconds

'''
      A
     ---
  F |   | B
     -G-
  E |   | C
     ---
      D

'''


class TM1637:
    I2C_COMM1 = 0x40
    I2C_COMM2 = 0xC0
    I2C_COMM3 = 0x80
    HEX_DIGIT_TO_SEGMENT = [
      # 0          1          2          3
        0b0111111, 0b0000110, 0b1011011, 0b1001111,
      # 4          5          6          7
        0b1100110, 0b1101101, 0b1111101, 0b0000111,
      # 8          9          A          b
        0b1111111, 0b1101111, 0b1110111, 0b1111100, 
      # C          d          E          F
        0b0111001, 0b1011110, 0b1111001, 0b1110001
        ]
    BOTTOM_TRANSITION = dict(zip(HEX_DIGIT_TO_SEGMENT, [
      # 0-         1-         2-         3-
        0b1010100, 0b0000100, 0b1001100, 0b1001100,
      # 4-         5-         6-         7-
        0b0011100, 0b1011000, 0b1011000, 0b1000100,
      # 8-         9-         A          b-
        0b1011100, 0b1011100, 0b1011100, 0b0011000, 
      # C-         d-         E-         F-
        0b1010000, 0b0001100, 0b1011000, 0b1011000
        ] ))
    BOTTOM_TRANSITION.update({0:0})
    ASCII_TO_SEGMENT = [
      # NUL   SOH   STX   ETX   EOT   ENQ   ACK   BEL   BS    HT    LF    VT
        0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
      # FF    CR    SO    SI    DLE   DC1   DC2   DC3   DC4   NAK   SYN   ETB
        0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
      # CAN   EM    SUB   ESC   FS    GS    RS    US    space !     "     #
        0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0x22, 0,
      # $     %     &     '     (     )     *     +     ,     -     .     /
        0,    0,    0,    0x01, 0,    0,    0,    0,    0x08, 0x40, 0x08, 0x52,
      # 0     1     2     3     4     5     6     7     8     9     :     ;
        0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F, 0,    0,
      # <     =     >     ?     @     A     B     C     D     E     F     G
        0,    0x48, 0,    0,    0,    0x77, 0x7C, 0x39, 0x5E, 0x79, 0x71, 0x3D,
      # H     I     J     K     L     M     N     O     P     Q     R     S
        0x76, 0x30, 0x1E, 0x75, 0x38, 0x55, 0x54, 0x5C, 0x73, 0x67, 0x50, 0x6D,
      # T     U     V     W     X     Y     Z     [     \     ]     ^     _
        0x78, 0x3E, 0x1C, 0x1D, 0x64, 0x6E, 0x5B, 0,    0x64, 0,    0,    0x08,
      # `     a     b     c     d     e     f     g     h     i     j     k
        0,    0x77, 0x7C, 0x39, 0x5E, 0x79, 0x71, 0x3D, 0x76, 0x30, 0x1E, 0x75,
      # l     m     n     o     p     q     r     s     t     u     v     w
        0x38, 0x55, 0x54, 0x5C, 0x73, 0x67, 0x50, 0x6D, 0x78, 0x3E, 0x1C, 0x1D,
      # x     y     z     {     |     }     ~     DEL
        0x64, 0x6E, 0x5B, 0,    0,    0,    0,    0
        ]
        
    def __init__(self, clk, dio, brightness):
        self.clk = clk
        self.dio = dio
        self.brightness = brightness

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




def show_text_sliding(tm, text, delay):
        segments = [0,0,0,0]
        for i in range(len(text)):
            segments[0] = segments[1]
            segments[1] = segments[2]
            segments[2] = segments[3]
            segments[3] = tm.ASCII_TO_SEGMENT[ord(text[i:i+1])]
            tm.set_segments(segments)
            sleep(delay)
        for i in range(4):
            segments[0] = segments[1]
            segments[1] = segments[2]
            segments[2] = segments[3]
            segments[3] = 0
            tm.set_segments(segments)
            sleep(delay)

def show_ip_address(tm, delay):
        text = str(subprocess.check_output("hostname -I", shell=True).strip(), encoding="ascii")
        show_text_sliding(tm, "IP "+text, delay)

def show_clock(tm, duration, delay):
        segments = [0,0,0,0]
        fsegments = [0,0,0,0]
        t = localtime()
        fsegments[0] = tm.HEX_DIGIT_TO_SEGMENT[t.tm_hour // 10] if t.tm_hour // 10 else 0
        fsegments[1] = tm.HEX_DIGIT_TO_SEGMENT[t.tm_hour % 10]
        fsegments[2] = tm.HEX_DIGIT_TO_SEGMENT[t.tm_min // 10]
        fsegments[3] = tm.HEX_DIGIT_TO_SEGMENT[t.tm_min % 10]
        for i in range(4):
            segments[3-i] = tm.BOTTOM_TRANSITION[fsegments[3-i]]
            tm.set_segments(segments)
            sleep(delay)
            segments[3-i] = fsegments[3-i]
            tm.set_segments(segments)
            sleep(delay)
        for i in range(int(duration)):
            t = localtime()
            sleep(1 - time() % 1)
            segments[0] = tm.HEX_DIGIT_TO_SEGMENT[t.tm_hour // 10] if t.tm_hour // 10 else 0
            segments[1] = tm.HEX_DIGIT_TO_SEGMENT[t.tm_hour % 10]
            segments[2] = tm.HEX_DIGIT_TO_SEGMENT[t.tm_min // 10]
            segments[3] = tm.HEX_DIGIT_TO_SEGMENT[t.tm_min % 10]
            tm.set_segments([segments[0], 0x80 + segments[1], segments[2], segments[3]])
            sleep(.5)
            tm.set_segments([segments[0], segments[1], segments[2], segments[3]])
        for i in range(4):
            segments[3-i] = tm.BOTTOM_TRANSITION[segments[3-i]]
            tm.set_segments(segments)
            sleep(delay)
            segments[3-i] = 0
            tm.set_segments(segments)
            sleep(delay)

def show_on_full_storage(tm, threshold_percent, delay):
        text = str(subprocess.check_output("df | sed 1d | sort -srnk 5 | tr -d '%' | tr -s ' ' ',' | cut -d, -f1,5", shell=True).strip(), encoding="ascii").split("\n")
        for row in range(len(text)):
            if int(text[row].split(",")[1]) >= threshold_percent:
                show_text_sliding(tm, text[row].split(",")[0]+" full", delay)

def show_on_low_memory(tm, threshold_kib, delay):
        text = int(str(subprocess.check_output("cat /proc/meminfo | grep MemA | cut -d':' -f2 | cut -c-11", shell=True).strip(), encoding="ascii"))
        if text < threshold_kib:
            show_text_sliding(tm, "ram "+str(text//1024)+" MiB left", delay)

def show_on_high_cpu_thermal(tm, threshold_celsius, delay):
        text = int(str(subprocess.check_output("cat /sys/devices/virtual/thermal/thermal_zone0/temp", shell=True).strip(), encoding="ascii"))
        if text >= threshold_celsius*1000:
            show_text_sliding(tm, "cpu high "+str(text//1000)+" C", delay)

def show_on_users(tm, delay):
        text = str(subprocess.check_output("uptime", shell=True).strip(), encoding="ascii").split(",")[1]
        if "  0 users" != text:
            show_text_sliding(tm, text, delay)

def show_on_stopped_process(tm, process_name, delay):
        text = str(subprocess.check_output(f"service {process_name} status", shell=True).strip(), encoding="utf8")
        if "running" not in text:
            show_text_sliding(tm, f"{process_name} stopped", ANIM_DELAY)

def demo(tm):
        # some commands might not work as intended depending on your architecture and distro
        while True:
            show_clock(tm, 20, ANIM_DELAY)
            show_ip_address(tm, ANIM_DELAY)
            #show_on_stopped_process(tm, "lighttpd", ANIM_DELAY)
            #show_on_stopped_process(tm, "mysql", ANIM_DELAY)
            #show_on_stopped_process(tm, "php7.4-fpm", ANIM_DELAY)
            show_on_high_cpu_thermal(tm, 60, ANIM_DELAY)
            show_on_low_memory(tm, 131072, ANIM_DELAY)
            show_on_full_storage(tm, 85, ANIM_DELAY)
            show_on_users(tm, ANIM_DELAY)
            sleep(20)

if __name__ == "__main__":
    gpio_clk = GPIO(CLK, "out")
    gpio_dio = GPIO(DIO, "out")

    tm = TM1637(CLK, DIO, BRIGHT)

    try:
        demo(tm)

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt")

    tm.set_segments([0,0,0,0])
    gpio_clk.close()
    gpio_dio.close()
