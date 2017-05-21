#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time
from datetime import timedelta
from typing import Dict, List
from pyrrigate.PyrrigateConfig_pb2 import RoutineConf
from pyrrigate.actions import RoutineAction
from pyrrigate.controllers import Controller
from pyrrigate.schedule import RoutineSchedule
from pyrrigate.settings import get_default_config


class Routine(object):
    @staticmethod
    def from_config(conf: RoutineConf, controllers: Dict[str, Controller]):
        """Creates a Routine object from the configuration"""
        actions = [RoutineAction.from_config(action, controllers)
                   for action in conf.action]
        return Routine(conf.id, actions)

    def __init__(self, routine_id: str, actions: List[RoutineAction]):
        self.routine_id = routine_id
        self.actions = actions

    def execute(self):
        """Runs all actions associated with the routine."""
        for action in self.actions:
            action.execute()


class RoutineController(object):
    """Dispatches the execution of routines based on a routine schedule."""

    def __init__(self, schedule: RoutineSchedule):
        self.schedule = schedule
        self.ran_events = set()

    def run(self):
        """Loop for fetching scheduled events and triggering unique executions."""
        import pyrrigate.util  # FIXME

        refresh_time = timedelta(seconds=10.0)
        while True:
            events = [e for e in self.schedule.refresh_next_events(refresh_time)
                      if e.event_id not in self.ran_events]

            # if there are not incoming events, sleep and refresh
            if not events:
                time.sleep(refresh_time.total_seconds())
                continue

            # builds the necessary objects from configuration files
            config = get_default_config()
            routines = pyrrigate.util.make_routine_dictionary(config)

            for event in events:
                self.ran_events.add(event.event_id)

                routine = routines.get(event.name)
                if routine is None:
                    logging.error("Ignoring unconfigured routine received from schedule.")
                    continue
                routine.execute()
