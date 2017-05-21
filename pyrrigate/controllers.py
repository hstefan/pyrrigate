#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
import logging
from pyrrigate.PyrrigateConfig_pb2 import ControllerConf
from pyrrigate.gpio import digital_write


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
        raise NotImplementedError

    @abc.abstractclassmethod
    def deactivate(self):
        raise NotImplementedError


class DigitalPinController(Controller):
    def __init__(self, controller_id: str, pin: int, reverse: bool=False):
        super().__init__(controller_id)
        self.pin = pin
        self.reverse = reverse

    def activate(self):
        logging.info('Activating controller "%s".')
        digital_write(self.pin, not self.reverse)

    def deactivate(self):
        logging.info('Deactivating controller "%s".')
        digital_write(self.pin, self.reverse)
