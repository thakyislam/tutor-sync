from accounts.models import Notification


def notify(recipient, title, message, link=''):
    return Notification.objects.create(
        recipient=recipient,
        title=title,
        message=message,
        link=link,
    )
