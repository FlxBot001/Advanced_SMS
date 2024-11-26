from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Q, F, Sum, Case, When, Value, IntegerField, Subquery, Max, Min
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from django.core.cache import cache
from rest_framework.parsers import MultiPartParser
from .tasks import process_voice_input
import os
from django.conf import settings
from celery.result import AsyncResult

from students.models import Student
from teachers.models import Teacher
from courses.models import Course
from attendance.models import Attendance
from cocurricular.models import CocurricularActivity
from behavior.models import BehaviorRecord
from .permissions import CanViewStudentReports
from dashboard.models import Message

@login_required
def dashboard(request):
    """Main dashboard view showing overall school statistics and metrics"""
    
    # Basic statistics
    context = {
        'total_students': Student.objects.count(),
        'total_teachers': Teacher.objects.count(),
        'total_courses': Course.objects.count(),
    }

    # Recent activity statistics with optimized queries
    context.update({
        'recent_students': Student.objects.select_related('user')
            .order_by('-created_at')[:5],
        'recent_teachers': Teacher.objects.select_related('user')
            .order_by('-created_at')[:5],
        'recent_courses': Course.objects.select_related('teacher')
            .order_by('-created_at')[:5],
    })

    # Distribution and analytics
    context.update({
        # Student analytics
        'student_grade_distribution': Student.objects.values('grade')
            .annotate(count=Count('id'))
            .order_by('grade'),
        
        # Teacher analytics
        'teacher_subject_distribution': Teacher.objects.values('subject')
            .annotate(count=Count('id'))
            .order_by('subject'),
        
        # Course analytics
        'course_enrollment_stats': Course.objects.annotate(
            student_count=Count('students'),
            average_grade=Avg('students__grade')
        ).order_by('-student_count')[:10],
        
        # Time-based analytics
        'new_students_this_week': Student.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).count(),
        'new_courses_this_month': Course.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).count(),
    })

    # Performance metrics
    context.update({
        'top_performing_courses': Course.objects.annotate(
            avg_grade=Avg('students__grade')
        ).order_by('-avg_grade')[:5],
        'most_active_teachers': Teacher.objects.annotate(
            course_count=Count('courses')
        ).order_by('-course_count')[:5],
    })

    return render(request, 'dashboard/dashboard.html', context)


class StudentReportDashboardView(APIView):
    """API view for detailed student reports"""
    permission_classes = [IsAuthenticated, CanViewStudentReports]
    
    def get(self, request, student_id):
        student = get_object_or_404(Student, id=student_id)
        
        # Time range filters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        # Base querysets with date filtering if provided
        attendance_qs = Attendance.objects.filter(student=student)
        cocurricular_qs = CocurricularActivity.objects.filter(student=student)
        behavior_qs = BehaviorRecord.objects.filter(student=student)
        
        if start_date and end_date:
            date_filter = {'date__range': [start_date, end_date]}
            attendance_qs = attendance_qs.filter(**date_filter)
            cocurricular_qs = cocurricular_qs.filter(**date_filter)
            behavior_qs = behavior_qs.filter(**date_filter)

        # Calculate statistics
        attendance_stats = {
            'total_days': attendance_qs.count(),
            'present_days': attendance_qs.filter(is_present=True).count(),
            'absence_rate': attendance_qs.filter(is_present=False).count() / max(attendance_qs.count(), 1) * 100
        }

        data = {
            "student": {
                "id": student.id,
                "name": student.user.get_full_name(),
                "grade": student.grade,
                "enrollment_date": student.created_at,
            },
            "attendance": {
                "stats": attendance_stats,
                "records": [
                    {"date": record.date, "present": record.is_present}
                    for record in attendance_qs
                ],
            },
            "cocurricular": {
                "total_activities": cocurricular_qs.count(),
                "records": [
                    {
                        "activity": activity.name,
                        "date": activity.date,
                        "performance": activity.performance if hasattr(activity, 'performance') else None
                    }
                    for activity in cocurricular_qs
                ],
            },
            "behavior": {
                "positive_count": behavior_qs.filter(is_positive=True).count(),
                "negative_count": behavior_qs.filter(is_positive=False).count(),
                "records": [
                    {
                        "description": record.description,
                        "date": record.date,
                        "positive": record.is_positive
                    }
                    for record in behavior_qs
                ],
            },
        }
        
        return Response(data)


class DashboardStatsView(APIView):
    """API endpoint for fetching dashboard statistics"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cache_key = f'dashboard_stats_{request.user.id}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)

        data = self.get_dashboard_stats()
        cache.set(cache_key, data, timeout=300)  # Cache for 5 minutes
        return Response(data)

    def get_dashboard_stats(self):
        return {
            'attendance_stats': self.get_attendance_stats(),
            'academic_stats': self.get_academic_stats(),
            'teacher_stats': self.get_teacher_stats(),
            'course_stats': self.get_course_stats()
        }

    def get_attendance_stats(self):
        today = timezone.now().date()
        return {
            'daily_attendance': Attendance.objects.filter(
                date=today
            ).aggregate(
                total=Count('id'),
                present=Count('id', filter=Q(is_present=True))
            ),
            'weekly_trend': Attendance.objects.filter(
                date__gte=today - timedelta(days=7)
            ).values('date').annotate(
                attendance_rate=Avg(Case(
                    When(is_present=True, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                ))
            )
        }

    def get_academic_stats(self):
        return {
            'grade_distribution': Student.objects.values('grade').annotate(
                count=Count('id'),
                avg_performance=Avg('academic_records__score')
            ),
            'top_performers': Student.objects.annotate(
                avg_score=Avg('academic_records__score')
            ).order_by('-avg_score')[:10]
        }

    def get_teacher_stats(self):
        return {
            'workload_distribution': Teacher.objects.annotate(
                course_load=Count('courses'),
                student_count=Count('courses__students')
            ).values('id', 'user__full_name', 'course_load', 'student_count'),
            'subject_coverage': Teacher.objects.values('subject').annotate(
                teacher_count=Count('id')
            )
        }

    def get_course_stats(self):
        return {
            'enrollment_trends': Course.objects.annotate(
                student_count=Count('students'),
                completion_rate=Avg(Case(
                    When(students__completion_status=True, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                ))
            )
        }


class StudentPerformanceView(APIView):
    """API endpoint for student performance metrics"""
    permission_classes = [IsAuthenticated, CanViewStudentReports]

    @action(detail=True, methods=['get'])
    def academic_progress(self, request, student_id):
        student = get_object_or_404(Student, id=student_id)
        
        return Response({
            'grades_trend': self.get_grades_trend(student),
            'subject_performance': self.get_subject_performance(student),
            'attendance_correlation': self.get_attendance_correlation(student)
        })

    def get_grades_trend(self, student):
        return student.academic_records.values(
            'date', 'subject'
        ).annotate(
            average_score=Avg('score')
        ).order_by('date')

    def get_subject_performance(self, student):
        return student.academic_records.values(
            'subject'
        ).annotate(
            average_score=Avg('score'),
            highest_score=Max('score'),
            lowest_score=Min('score')
        )

    def get_attendance_correlation(self, student):
        return student.academic_records.annotate(
            attendance_rate=Subquery(
                Attendance.objects.filter(
                    student=student,
                    date__month=F('academic_records__date__month')
                ).values('month').annotate(
                    rate=Avg(Case(
                        When(is_present=True, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    ))
                ).values('rate')
            )
        )


@login_required
def teacher_dashboard(request):
    """Dashboard view for teachers"""
    teacher = get_object_or_404(Teacher, user=request.user)
    
    context = {
        'current_courses': Course.objects.filter(
            teacher=teacher,
            is_active=True
        ).annotate(
            student_count=Count('students'),
            avg_performance=Avg('students__academic_records__score')
        ),
        'recent_submissions': Assignment.objects.filter(
            course__teacher=teacher
        ).order_by('-submission_date')[:10],
        'attendance_summary': self.get_teacher_attendance_summary(teacher),
        'upcoming_events': Event.objects.filter(
            Q(teacher=teacher) | Q(course__teacher=teacher),
            date__gte=timezone.now()
        ).order_by('date')[:5]
    }
    
    return render(request, 'dashboard/teacher_dashboard.html', context)

def get_teacher_attendance_summary(teacher):
    today = timezone.now().date()
    courses = teacher.courses.all()
    
    return Attendance.objects.filter(
        student__courses__in=courses,
        date=today
    ).aggregate(
        total_students=Count('student', distinct=True),
        present_students=Count('student', filter=Q(is_present=True)),
        absence_rate=1 - F('present_students') / F('total_students')
    )


@login_required
def student_dashboard(request):
    """Dashboard view for students"""
    student = get_object_or_404(Student, user=request.user)
    
    context = {
        'current_courses': student.courses.filter(
            is_active=True
        ).annotate(
            assignments_count=Count('assignments'),
            completed_assignments=Count(
                'assignments',
                filter=Q(assignments__status='completed')
            )
        ),
        'upcoming_assignments': Assignment.objects.filter(
            course__students=student,
            due_date__gte=timezone.now()
        ).order_by('due_date')[:5],
        'recent_grades': student.academic_records.order_by(
            '-date'
        )[:5],
        'attendance_record': student.attendance_set.filter(
            date__gte=timezone.now() - timedelta(days=30)
        ).order_by('-date')
    }
    
    return render(request, 'dashboard/student_dashboard.html', context)

@login_required
def profile_view(request):
    """User profile view"""
    context = {
        'user_profile': request.user,
        'recent_activities': get_user_activities(request.user)
    }
    return render(request, 'dashboard/profile.html', context)

@login_required
def settings_view(request):
    """User settings view"""
    if request.method == 'POST':
        # Handle settings update
        pass
    return render(request, 'dashboard/settings.html')

@login_required
def calendar_view(request):
    """Calendar view showing events and schedules"""
    context = {
        'events': Event.objects.filter(
            date__gte=timezone.now()
        ).order_by('date')[:10],
        'user_events': get_user_events(request.user)
    }
    return render(request, 'dashboard/calendar.html', context)

@login_required
def messages_view(request):
    """Messaging system view"""
    context = {
        'inbox': get_user_messages(request.user),
        'sent': get_user_sent_messages(request.user)
    }
    return render(request, 'dashboard/messages.html', context)

@login_required
def take_attendance(request):
    """View for teachers to take attendance"""
    if not hasattr(request.user, 'teacher'):
        return redirect('main-dashboard')
        
    if request.method == 'POST':
        # Handle attendance submission
        pass
        
    context = {
        'courses': request.user.teacher.courses.filter(is_active=True),
        'today_attendance': get_today_attendance(request.user.teacher)
    }
    return render(request, 'dashboard/take_attendance.html', context)

@login_required
def submit_assignment(request):
    """View for students to submit assignments"""
    if not hasattr(request.user, 'student'):
        return redirect('main-dashboard')
        
    if request.method == 'POST':
        # Handle assignment submission
        pass
        
    context = {
        'pending_assignments': get_pending_assignments(request.user.student),
        'submitted_assignments': get_submitted_assignments(request.user.student)
    }
    return render(request, 'dashboard/submit_assignment.html', context)

@login_required
def course_list(request):
    """View for listing all courses"""
    context = {
        'courses': Course.objects.filter(is_active=True)
    }
    return render(request, 'dashboard/course_list.html', context)

@login_required
def course_create(request):
    """View for creating new courses"""
    if not hasattr(request.user, 'teacher'):
        return redirect('course-list')
        
    if request.method == 'POST':
        # Handle course creation
        pass
        
    return render(request, 'dashboard/course_create.html')

# Helper functions
def get_user_activities(user):
    """Get recent activities for a user"""
    activities = []
    if hasattr(user, 'teacher'):
        activities.extend(user.teacher.courses.all()[:5])
    if hasattr(user, 'student'):
        activities.extend(user.student.academic_records.all()[:5])
    return activities

def get_user_events(user):
    """Get events relevant to the user"""
    events = Event.objects.filter(
        Q(is_school_wide=True) |
        Q(teacher=getattr(user, 'teacher', None)) |
        Q(course__in=getattr(user, 'student', None).courses.all() if hasattr(user, 'student') else [])
    ).distinct()
    return events

def get_user_messages(user):
    """Get user's received messages"""
    return Message.objects.filter(recipient=user).order_by('-created_at')

def get_user_sent_messages(user):
    """Get user's sent messages"""
    return Message.objects.filter(sender=user).order_by('-created_at')

def get_today_attendance(teacher):
    """Get today's attendance for teacher's courses"""
    return Attendance.objects.filter(
        student__courses__teacher=teacher,
        date=timezone.now().date()
    )

def get_pending_assignments(student):
    """Get pending assignments for a student"""
    return Assignment.objects.filter(
        course__students=student,
        due_date__gte=timezone.now(),
        status='pending'
    )

def get_submitted_assignments(student):
    """Get submitted assignments for a student"""
    return Assignment.objects.filter(
        course__students=student,
        status='completed'
    )

class VoiceInputView(APIView):
    """Handle voice input uploads and processing"""
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)
    
    def post(self, request):
        if 'audio' not in request.FILES:
            return Response(
                {'error': 'No audio file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        audio_file = request.FILES['audio']
        
        # Validate file type and size
        if audio_file.content_type not in settings.ALLOWED_AUDIO_TYPES:
            return Response(
                {'error': 'Invalid audio file type'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if audio_file.size > settings.MAX_AUDIO_SIZE:
            return Response(
                {'error': 'Audio file too large'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Save the file
        os.makedirs(settings.VOICE_UPLOAD_PATH, exist_ok=True)
        file_path = os.path.join(
            settings.VOICE_UPLOAD_PATH,
            f'voice_input_{request.user.id}_{timezone.now().timestamp()}.wav'
        )
        
        with open(file_path, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)
        
        # Process the voice input asynchronously
        task = process_voice_input.delay(file_path)
        
        return Response({
            'message': 'Voice input received and being processed',
            'task_id': task.id
        })
    
    def get(self, request):
        """Check the status of a voice processing task"""
        task_id = request.query_params.get('task_id')
        if not task_id:
            return Response(
                {'error': 'No task ID provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        task = AsyncResult(task_id)
        return Response({
            'status': task.status,
            'result': task.result if task.ready() else None
        })
