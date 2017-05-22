#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import argparse
from pyrrigate.gcall import GoogleCalendarFetcher, get_google_calendar_credentials
from pyrrigate.routine import RoutineController
from pyrrigate.schedule import RoutineSchedule
from pyrrigate.settings import get_default_config
from pyrrigate.util import make_controller_dictionary


def reset_controllers(dummy: bool):
    """Resets all configured controllers."""
    logging.info('Resetting all controllers.')
    config = get_default_config()
    controllers = make_controller_dictionary(config, dummy)
    for controller in controllers.values():
        controller.deactivate()


def init_gpio(dummy: bool=False):
    """Initializes wiringpi."""
    if dummy:
        return
    import wiringpi
    wiringpi.wiringPiSetup()


def parse_args():
    """Parses command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--use-dummy-gpio', default=False, action='store_true')
    return parser.parse_args()


def main():
    # set up loggers
    logging.basicConfig(level=logging.INFO)
    googleapi_logger = logging.getLogger('googleapiclient')
    if googleapi_logger:
        googleapi_logger.setLevel(logging.ERROR)

    logging.info('Initializing Pyrrigate.')
    args = parse_args()

    init_gpio(args.use_dummy_gpio)
    config = get_default_config()
    # deactivates all controllers
    reset_controllers(args.use_dummy_gpio)
    try:
        gcal_creds = get_google_calendar_credentials(config.googleCalendar)
        gcal = GoogleCalendarFetcher(config.googleCalendar, gcal_creds)
        schedule = RoutineSchedule(gcal)
        routine_controller = RoutineController(schedule, args.use_dummy_gpio)
        routine_controller.run()
    except:  # if anything goes wrong, deactivate all controllers
        reset_controllers(args.use_dummy_gpio)


if __name__ == '__main__':
    main()
