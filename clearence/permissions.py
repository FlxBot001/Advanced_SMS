from rest_framework import permissions

class CanApproveClearance(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('clearance.can_approve_clearance') 