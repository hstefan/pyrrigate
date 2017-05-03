googleCalendar {
  secretFilePath: "client_secret.json"
  credentialsPath: "~/.credentials/pyrrigate-gcalendar-poller.json"
  calendarId: "YOUR_CALENDAR_ID"
}
controller {
  id: "left_hose"
  type: CONTROLLER_DIGITAL_PIN
}
controller {
  id: "center_hose"
  type: CONTROLLER_DIGITAL_PIN
  pinNumber: 1
}
routine {
  id: "summer"
  action {
    actionType: ACTION_ENABLE_TIMED
    targetController: "left_hose"
    enabledTime: 60.0
  }
  action {
    actionType: ACTION_ENABLE_TIMED
    targetController: "center_hose"
    enabledTime: 90.0
  }
}
routine {
  id: "winter"
  action {
    actionType: ACTION_ENABLE_TIMED
    targetController: "left_hose"
    enabledTime: 30.0
  }
  action {
    actionType: ACTION_ENABLE_TIMED
    targetController: "center_hose"
    enabledTime: 60.0
  }
}
