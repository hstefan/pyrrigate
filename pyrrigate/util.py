#!/usr/bin/env python3
# -*- coding; utf-8 -*-

from typing import Dict

from pyrrigate.PyrrigateConfig_pb2 import PyrrigateConf
import pyrrigate.controllers
import pyrrigate.routine

ControllerDict = Dict[str, pyrrigate.controllers.Controller]
RoutineDict = Dict[str, pyrrigate.routine.Routine]

def make_controller_dictionary(config: PyrrigateConf, dummy: bool=False) -> ControllerDict:
    """Makes a dictionary associating controller ids to their concrete types."""
    return {c.id: pyrrigate.controllers.Controller.from_config(c, dummy)
            for c in config.controller}


def make_routine_dictionary(config: PyrrigateConf, controllers: ControllerDict) -> RoutineDict:
    """Makes a dictionary associating routine ids to their concrete types.
    If :param: controllers isn't set, a dictionary of controllers is internally built using 
    :func: make_controller_dictionary.
    """
    if not controllers:
        controllers = make_controller_dictionary(config)
    return {r.id: pyrrigate.routine.Routine.from_config(r, controllers)
            for r in config.routine}
