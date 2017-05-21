#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

try:
    import wiringpi
except ModuleNotFoundError:
    logging.warning('wiringpi is not installed, gpio calls will only be mocked.')


def init():
    try:
        wiringpi.wiringPiSetup()
    except NameError:
        logging.info('gpio.wiringPiSetup()')


def digital_write(pin: int, value: bool):
    logging.info('gpio.digital_write(%d, %r)', pin, value)
    try:
        wiringpi.digitalWrite(pin, wiringpi.HIGH if value else wiringpi.LOW)
    except NameError:
        pass
