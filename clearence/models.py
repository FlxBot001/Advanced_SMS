from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class ClearanceRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clearance_requests')
    resource = models.CharField(max_length=100)
    reason = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    approved = models.BooleanField(default=False)
    approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_clearances')
    
    def __str__(self):
        return f"{self.user.username} - {self.resource} - {self.start_time}"

class ClearanceLog(models.Model):
    clearance = models.ForeignKey(ClearanceRequest, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(max_length=50)  # e.g., "accessed", "exited"
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.clearance.user.username} - {self.clearance.resource} - {self.action}"

