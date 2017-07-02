#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from time import sleep
import socket

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

inchan = [12, 16]
outchan = [20, 21]
lightswitch = 12
printerswitch = 16
printerled = 20
lightled = 21

GPIO.setup(inchan, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(outchan, GPIO.OUT, initial=GPIO.LOW)


def writefile(s):
    fo = open(".gpio.state", "w")
    fo.write(s)
    fo.close()


def edgechange(channel):
    GPIO.remove_event_detect(channel)
    if channel is printerswitch:
        print "printerswitch"
        GPIO.output(printerled, GPIO.input(printerswitch))
        sendsocket('10.10.11.72', 9970, str(GPIO.input(printerswitch)))
    elif channel is lightswitch:
        print "lightswitch"
        GPIO.output(lightled, GPIO.input(lightswitch))

    if GPIO.input(channel):
        GPIO.add_event_detect(channel, GPIO.FALLING, callback=falling,
                              bouncetime=300)
    else:
        GPIO.add_event_detect(channel, GPIO.RISING, callback=rising,
                              bouncetime=300)


def sendsocket(host, port, msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(msg)
    s.close()


def falling(channel):
    print "0"
    writefile("0")
    edgechange(channel)


def rising(channel):
    print "1"
    writefile("1")
    edgechange(channel)


for switch in inchan:
    if GPIO.input(switch):
        GPIO.add_event_detect(switch, GPIO.FALLING, callback=falling,
                              bouncetime=300)
        writefile("1")
    else:
        GPIO.add_event_detect(switch, GPIO.RISING, callback=rising,
                              bouncetime=300)
        writefile("0")

try:
    while True:
        sleep(2)
except KeyboardInterrupt:
    print("user aborted script...")
finally:
    GPIO.cleanup()
