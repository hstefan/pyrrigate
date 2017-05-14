googleCalendar {
  secretFilePath: "client_secret.json"
  credentialsPath: "~/.credentials/pyrrigate-gcalendar-poller.json"
  calendarId: "0unckm6l2ecvnrl96ej96mkf9c@group.calendar.google.com"
}
controller {
  id: "left_hose"
  type: CONTROLLER_DIGITAL_PIN
  pinNumber: 0
  reversed: true
}
controller {
  id: "center_hose"
  type: CONTROLLER_DIGITAL_PIN
  pinNumber: 1
  reversed: true
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
