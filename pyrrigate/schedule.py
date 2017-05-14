#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import logging
from typing import NamedTuple, List
from datetime import timedelta, datetime
from dateutil.parser import parse as date_parse
from pyrrigate.gcall import GoogleCalendarFetcher


class RoutineEvent(NamedTuple):
    event_id: str
    name: str
    start_utc: datetime


class RoutineSchedule(object):
    """Builds RoutineEvent fetched from a schedule provider (e.g. Google Calendar).
    
    Google Calendar events are currently the only type supported, and rely on the syntax
    'routine:name' in the event summary to define which routine should be run at a given start
    time.
    """
    def __init__(self, gcal: GoogleCalendarFetcher):
        self.gcal = gcal
        self.re_extract = re.compile(r'^\s*routine\s*:\s*(\w+)+\s*$', re.IGNORECASE)

    def refresh_next_events(self, lookahead_time: timedelta) -> List[RoutineEvent]:
        """Refreshes the list of scheduled events.
        
        Parses summary events that are returned by the calendar fetcher, in the time range 
        between utc now and utc now + lookahead_time.   
        """
        # TODO: should we handle events with the same id but that were rescheduled?
        events = []
        for event in self.gcal.fetch(lookahead_time):
            summary = event['summary']
            parse_match = self.re_extract.search(summary)

            if not parse_match:
                logging.warning('Event "%s" does not match a routine description, skipping!')
                continue

            start_date = date_parse(event['start']['dateTime'])
            routine_name = parse_match.group(1)
            routine_event = RoutineEvent(event['id'], routine_name, start_date)
            events.append(routine_event)

        return events
