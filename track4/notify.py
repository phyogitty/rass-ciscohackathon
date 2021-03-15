from notifypy import Notify
def user(msg):
    notification = Notify()
    notification.title = "From {}".format(msg['from'])
    notification.message = "{}".format(msg['summary'])
    notification.icon = "logo-rass.png"
    notification.application_name = "Marked As Useful Email"
    notification._notification_icon = "logo-rass.png"
    notification.send()