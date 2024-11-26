from rest_framework import serializers
from .models import Course, Subject, Strand, SubStrand, LearningOutcome

class LearningOutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningOutcome
        fields = '__all__'

class SubStrandSerializer(serializers.ModelSerializer):
    learning_outcomes = LearningOutcomeSerializer(many=True, read_only=True)
    
    class Meta:
        model = SubStrand
        fields = '__all__'

class StrandSerializer(serializers.ModelSerializer):
    sub_strands = SubStrandSerializer(many=True, read_only=True)
    
    class Meta:
        model = Strand
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    strands = StrandSerializer(many=True, read_only=True)
    
    class Meta:
        model = Subject
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__' 