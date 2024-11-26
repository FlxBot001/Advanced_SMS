from rest_framework import permissions

class CanViewStudentReports(permissions.BasePermission):
    """
    Permission to check if user can view student reports.
    Allows access to teachers, admins, and students viewing their own data.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Admins can view all
        if request.user.is_staff:
            return True
            
        # Teachers can view their students
        if hasattr(request.user, 'teacher'):
            return True
            
        # Students can only view their own data
        if hasattr(request.user, 'student'):
            student_id = view.kwargs.get('student_id')
            return student_id == request.user.student.id
            
        return False 