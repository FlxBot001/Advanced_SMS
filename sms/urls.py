"""
URL configuration for sms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from students.views import StudentViewSet, StudentSubjectViewSet
from teachers.views import TeacherViewSet
from parents.views import ParentViewSet
from courses.views import CourseViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'student-subjects', StudentSubjectViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'parents', ParentViewSet)
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('clearance/', include('clearance.urls')),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('calendar/', views.calendar, name='calendar'),
    path('messages/', views.messages, name='messages'),

]
