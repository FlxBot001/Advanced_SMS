from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class RoleBasedPermissionBackend(ModelBackend):
    def has_perm(self, user_obj, perm, obj=None):
        if user_obj.is_active and user_obj.is_superuser:
            return True
        
        # Define role-based permissions
        role_permissions = {
            'principal': ['view_all', 'edit_all', 'approve_all'],
            'deputy_principal': ['view_all', 'edit_most', 'approve_most'],
            'senior_teacher': ['view_department', 'edit_department'],
            'department_head': ['view_department', 'edit_department'],
            'class_teacher': ['view_class', 'edit_class'],
            'lab_technician': ['view_lab', 'edit_lab'],
            'secretary': ['view_admin', 'edit_admin'],
            'treasurer': ['view_finance', 'edit_finance'],
            'student_leader': ['view_student_affairs'],
            'teacher': ['view_assigned', 'edit_assigned'],
            'student': ['view_own'],
            'parent': ['view_child'],
        }
        
        if user_obj.role in role_permissions:
            return perm in role_permissions[user_obj.role]
        
        return False

