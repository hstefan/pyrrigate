#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A script that constantly polls Google Calendar for irrigation schedules."""

import datetime
import logging
import os
import os.path

import httplib2
from apiclient import discovery
from oauth2client import client, tools
from oauth2client.client import Credentials as OAuthCredentials
from oauth2client.file import Storage
from pyrrigate.PyrrigateConfig_pb2 import GoogleCalendarConf

# internal constants
_GCAL_SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
_GCAL_APPLICATION_NAME = 'Pyrrigate Google Calendar Poller'


class GoogleCalendarFetcher(object):
    """Polls Google Calendar events from the configured calendar."""

    def __init__(self, conf: GoogleCalendarConf, credentials: OAuthCredentials):
        self.conf = conf
        self.http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=self.http)

    def fetch(self, delta: datetime.timedelta):
        """Retrieves all events from now until now + delta."""
        utc_now = datetime.datetime.utcnow().isoformat() + 'Z'
        utc_end = (datetime.datetime.utcnow() + delta).isoformat() + 'Z'

        events = self.service.events().list(calendarId=self.conf.calendarId,
                                            timeMin=utc_now, timeMax=utc_end,
                                            singleEvents=True, orderBy='startTime').execute()

        return events['items']


def get_google_calendar_credentials(conf: GoogleCalendarConf) -> OAuthCredentials:
    """
    Gets valid user credentials for google calendar, accordingly to the given settings.
    Returns:
        Credentials if file already exists or a new oauth flow is successfully ran. If neither 
        operation succeeds, returns None.
    """
    credential_path = os.path.expanduser(conf.credentialsPath)
    store = Storage(credential_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        logging.warning('Credentials not found at "%s"', credential_path)
        flow = client.flow_from_clientsecrets(conf.secretFilePath, _GCAL_SCOPES)
        flow.user_agent = _GCAL_APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        if not credentials or credentials.invalid:
            logging.error('Failed to run authentication flow.')
            return None

    return credentials
