from django.contrib import admin
from .models import ClearanceRequest, ClearanceLog

@admin.register(ClearanceRequest)
class ClearanceRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'resource', 'status', 'start_time', 'end_time']
    list_filter = ['status', 'resource']
    search_fields = ['user__username', 'resource', 'reason']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)
        return qs

@admin.register(ClearanceLog)
class ClearanceLogAdmin(admin.ModelAdmin):
    list_display = ['clearance', 'action', 'performed_by', 'timestamp']
    list_filter = ['action']
    search_fields = ['clearance__user__username', 'clearance__resource'] 