from notifypy import Notify

notification = Notify()
notification.title = "Moshi Moshi"
notification.message = "This is a message."
notification.icon = "../logo-rass.png"
notification.application_name = "Nofication from Rass"
notification._notification_icon = "../logo-rass.png"
notification.send()