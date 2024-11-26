from django.conf import settings
from django.db import connection
from .models import School

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        hostname = request.get_host().split(':')[0].lower()
        subdomain = hostname.split('.')[0]
        
        try:
            school = School.objects.get(subdomain=subdomain)
            request.school = school
            connection.schema_name = f'school_{school.id}'
        except School.DoesNotExist:
            connection.schema_name = 'public'
        
        response = self.get_response(request)
        return response

