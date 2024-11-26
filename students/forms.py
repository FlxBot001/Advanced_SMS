from django import forms
from .models import Student

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'grade', 'date_of_birth', 'address', 'phone_number']

    def clean_student_id(self):
        student_id = self.cleaned_data['student_id']
        if Student.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError("This student ID is already in use.")
        return student_id
    
    class StudentForm(forms.ModelForm):
        class Meta:
            model = Student
            fields = ['student_id', 'grade', 'enrollment_date']

    class StudentSubjectForm(forms.ModelForm):
        class Meta:
            model = StudentSubject
            fields = ['subject', 'grade', 'year']


