from .models import Notification


def notifications(request):
    if not request.user.is_authenticated:
        return {'unread_count': 0, 'recent_notifications': []}
    unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    recent_notifications = Notification.objects.filter(recipient=request.user)[:5]
    return {
        'unread_count': unread_count,
        'recent_notifications': recent_notifications,
    }
