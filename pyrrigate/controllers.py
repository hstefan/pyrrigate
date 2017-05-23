#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
import logging
try:
    import wiringpi
except ModuleNotFoundError:
    logging.warning('wiringpi is not installed! This should only be used with --use-dummy-gpio.')

from pyrrigate.PyrrigateConfig_pb2 import ControllerConf

class Controller(metaclass=abc.ABCMeta):
    @staticmethod
    def from_config(conf: ControllerConf, dummy=False):
        """Creates a controller object for the given configuration."""
        # TODO: more controller types
        assert conf.type == ControllerConf.CONTROLLER_DIGITAL_PIN
        return DigitalPinController(conf.id, conf.pinNumber, conf.reversed, dummy)

    def __init__(self, controller_id):
        self.controller_id = controller_id

    @abc.abstractclassmethod
    def activate(self):
        raise NotImplementedError

    @abc.abstractclassmethod
    def deactivate(self):
        raise NotImplementedError

    @abc.abstractclassmethod
    def configure(self):
        raise NotImplementedError


class DigitalPinController(Controller):
    def __init__(self, controller_id: str, pin: int, reverse: bool=False, dummy=False):
        super().__init__(controller_id)
        self.pin = pin
        self.reverse = reverse
        self.dummy = dummy

    def activate(self):
        logging.info('Activating controller "%s".', self.controller_id)
        self._digital_write(not self.reverse)

    def deactivate(self):
        logging.info('Deactivating controller "%s".', self.controller_id)
        self._digital_write(self.reverse)

    def _digital_write(self, value: bool):
        if self.dummy:
            logging.info('digital_write(%d, %r)', self.pin, value)
        else:
            wiringpi.digitalWrite(self.pin, wiringpi.HIGH if value else wiringpi.LOW)

    def configure(self):
        if self.dummy:
            logging.info('pin_mode(%d, OUTPUT)', self.pin)
        else:
            wiringpi.pinMode(self.pin, wiringpi.OUTPUT)
