from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .forms import StudentForm, StudentSubjectForm
from .models import Student


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['grade']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    ordering_fields = ['user__username', 'grade']
    ordering = ['user__username']
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create_student(request):
        if request.method == 'POST':
            form = StudentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('student_list')
        else:
            form = StudentForm()
        return render(request, 'students/create_student.html', {'form': form})

    def add_student_subject(request, student_id):
        student = Student.objects.get(pk=student_id)
        if request.method == 'POST':
            form = StudentSubjectForm(request.POST)
            if form.is_valid():
                subject = form.save(commit=False)
                subject.student = student
                subject.save()
                return redirect('student_detail', student_id=student_id)
        else:
            form = StudentSubjectForm()
        return render(request, 'students/add_subject.html', {'form': form, 'student': student})

