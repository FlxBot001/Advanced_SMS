from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, Subject, Strand, SubStrand, LearningOutcome
from .serializers import (
    CourseSerializer, 
    SubjectSerializer, 
    StrandSerializer,
    SubStrandSerializer,
    LearningOutcomeSerializer
)
from core.permissions import IsTeacherOrReadOnly

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsTeacherOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code', 'learning_area', 'grade_level']

class StrandViewSet(viewsets.ModelViewSet):
    queryset = Strand.objects.all()
    serializer_class = StrandSerializer
    permission_classes = [IsTeacherOrReadOnly]

class SubStrandViewSet(viewsets.ModelViewSet):
    queryset = SubStrand.objects.all()
    serializer_class = SubStrandSerializer
    permission_classes = [IsTeacherOrReadOnly]

class LearningOutcomeViewSet(viewsets.ModelViewSet):
    queryset = LearningOutcome.objects.all()
    serializer_class = LearningOutcomeSerializer
    permission_classes = [IsTeacherOrReadOnly]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code', 'subject__name', 'term', 'academic_year']

    @action(detail=True, methods=['get'])
    def learning_outcomes(self, request, pk=None):
        course = self.get_object()
        outcomes = LearningOutcome.objects.filter(
            sub_strand__strand__subject=course.subject
        )
        serializer = LearningOutcomeSerializer(outcomes, many=True)
        return Response(serializer.data)

