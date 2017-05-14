#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyrrigate.settings import get_default_config
from pyrrigate.gcall import GoogleCalendarFetcher, get_google_calendar_credentials
from pyrrigate.routine import RoutineController
from pyrrigate.schedule import RoutineSchedule


def main():
    config = get_default_config()
    gcal_creds = get_google_calendar_credentials(config.googleCalendar)
    gcal = GoogleCalendarFetcher(config.googleCalendar, gcal_creds)
    schedule = RoutineSchedule(gcal)
    routine_controller = RoutineController(schedule)
    routine_controller.run()

if __name__ == '__main__':
    main()
