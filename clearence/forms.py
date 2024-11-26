from django import forms
from .models import ClearanceRequest

class ClearanceRequestForm(forms.ModelForm):
    class Meta:
        model = ClearanceRequest
        fields = ['resource', 'reason', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        } 