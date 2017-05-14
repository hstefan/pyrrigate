#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
import wiringpi
from pyrrigate.PyrrigateConfig_pb2 import ControllerConf


class Controller(metaclass=abc.ABCMeta):
    @staticmethod
    def from_config(conf: ControllerConf):
        """Creates a controller object for the given configuration."""
        # TODO: more controller types
        assert conf.type == ControllerConf.CONTROLLER_DIGITAL_PIN
        return DigitalPinController(conf.id, conf.pinNumber, conf.reversed)

    def __init__(self, controller_id):
        self.controller_id = controller_id

    @abc.abstractclassmethod
    def activate(self):
        pass

    @abc.abstractclassmethod
    def deactivate(self):
        pass


class DigitalPinController(Controller):
    def __init__(self, controller_id: str, pin: int, reverse: bool = False):
        super().__init__(controller_id)
        self.pin = pin
        self.reverse = reverse

    def activate(self):
        active_value = wiringpi.LOW if self.reverse else wiringpi.HIGH
        wiringpi.digitalWrite(active_value)

    def deactivate(self):
        inactive_value = wiringpi.HIGH if self.reverse else wiringpi.LOW
        wiringpi.digitalWrite(inactive_value)
