#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
import time
import logging
from typing import List, Dict


from pyrrigate.PyrrigateConfig_pb2 import RoutineActionConf
from pyrrigate.controllers import Controller


class RoutineAction(metaclass=abc.ABCMeta):
    """
    Abstract representation of the possible routine actions.
     
    Defines both the interface
    """
    # TODO: we should have an async version of the execute method to allow aborting?

    @staticmethod
    def from_config(conf: RoutineActionConf, controllers: Dict[str, Controller]):
        """Builds concrete RoutineAction from a given configuration and a list of known controllers.
        :return: a concrete type for the specific action extracted from conf.actionType.
        """
        # TODO: more action types
        assert conf.actionType == RoutineActionConf.ACTION_ENABLE_TIMED

        target_ids = set(conf.targetController)
        target_controllers = [controllers[c] for c in target_ids]

        assert len(target_controllers) == len(target_ids)  # were all controllers found?

        return TimedEnableAction(target_controllers, conf.enabledTime)

    @abc.abstractmethod
    def execute(self):
        """Executes the desired action, blocking until it's finished or fails.
        :return: True is the action was successful, False otherwise.
        """


class TimedEnableAction(RoutineAction):
    """Enables all target controllers for a number of seconds, resetting them afterwards."""

    def __init__(self, target_controllers: List[Controller], enabled_time: float):
        self.target_controllers = target_controllers
        self.enabled_time = enabled_time

    def execute(self):
        logging.info('Enabling %s controllers for %f seconds',
                     [c.controller_id for c in self.target_controllers],
                     self.enabled_time)
        try:
            for controller in self.target_controllers:
                controller.activate()
            time.sleep(self.enabled_time)
            return True
        except Exception as e:
            logging.exception('Exception caught during execution of action.', e)
            return False
