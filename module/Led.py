#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# GPIO25を出力としてLEDに給電する
import RPi.GPIO as GPIO
from time import sleep

LED_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

while True:
    GPIO.output(LED_PIN, GPIO.HIGH)
    sleep(0.5)
    GPIO.output(LED_PIN, GPIO.LOW)
    sleep(0.5)
