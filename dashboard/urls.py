from django.urls import path
from . import views
from .views import VoiceInputView

urlpatterns = [
    # Main Dashboards
    path('', views.dashboard, name='main-dashboard'),
    path('teacher/', views.teacher_dashboard, name='teacher-dashboard'),
    path('student/', views.student_dashboard, name='student-dashboard'),
    
    # User Management
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    
    # Features
    path('calendar/', views.calendar_view, name='calendar'),
    path('messages/', views.messages_view, name='messages'),
    path('take-attendance/', views.take_attendance, name='take-attendance'),
    path('submit-assignment/', views.submit_assignment, name='submit-assignment'),
    
    # Course Management
    path('courses/', views.course_list, name='course-list'),
    path('courses/create/', views.course_create, name='course-create'),
    
    # API Endpoints
    path('api/stats/', views.DashboardStatsView.as_view(), name='dashboard-stats'),
    path('api/student/<int:student_id>/performance/', 
         views.StudentPerformanceView.as_view(), name='student-performance'),
    path('voice-input/', VoiceInputView.as_view(), name='voice-input'),
] 