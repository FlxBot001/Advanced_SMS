from django.test import TestCase
from django.contrib.auth.models import User
from .models import Student, StudentSubject

class StudentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.student = Student.objects.create(
            user=self.user,
            student_id='S12345',
            grade='10'
        )

    def test_student_creation(self):
        self.assertTrue(isinstance(self.student, Student))
        self.assertEqual(self.student.__str__(), 'testuser - S12345')

class StudentAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)
        self.student = Student.objects.create(
            user=self.user,
            student_id='S12345',
            grade='10'
        )

    def test_get_students(self):
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

