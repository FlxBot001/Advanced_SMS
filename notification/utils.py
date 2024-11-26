from .models import Notification
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

def send_notification(recipient, message, related_object=None):
    notification = Notification(
        recipient=recipient,
        message=message
    )
    
    if related_object:
        content_type = ContentType.objects.get_for_model(related_object)
        notification.content_type = content_type
        notification.object_id = related_object.id
    
    notification.save()
    
    # Here you can add logic to send real-time notifications
    # For example, using Django Channels

