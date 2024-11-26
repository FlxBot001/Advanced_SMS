from django.core.exceptions import PermissionDenied
from .models import ClearanceRequest

class ClearanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Check if the user needs clearance for the requested resource
            resource = self.get_resource_from_path(request.path)
            if resource and not self.has_clearance(request.user, resource):
                raise PermissionDenied
        return self.get_response(request) 