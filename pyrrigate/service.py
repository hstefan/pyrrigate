#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

import pyrrigate.gpio as gpio
from pyrrigate.gcall import GoogleCalendarFetcher, get_google_calendar_credentials
from pyrrigate.routine import RoutineController
from pyrrigate.schedule import RoutineSchedule
from pyrrigate.settings import get_default_config
from pyrrigate.util import make_controller_dictionary


def reset_controllers():
    """Resets all configured controllers."""
    logging.info('Resetting all controllers.')
    config = get_default_config()
    controllers = make_controller_dictionary(config)
    for controller in controllers.values():
        controller.deactivate()


def main():
    logging.info('Initializing Pyrrigate.')
    gpio.init()
    config = get_default_config()
    # deactivates all controllers
    reset_controllers()
    try:
        gcal_creds = get_google_calendar_credentials(config.googleCalendar)
        gcal = GoogleCalendarFetcher(config.googleCalendar, gcal_creds)
        schedule = RoutineSchedule(gcal)
        routine_controller = RoutineController(schedule)
        routine_controller.run()
    except:  # if anything goes wrong, deactivate all controllers
        reset_controllers()


if __name__ == '__main__':
    main()
