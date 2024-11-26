from celery import shared_task
from .ml_model import train_model, predict_score
from students.models import Student
from .models import StudentPrediction
import pandas as pd

@shared_task
def train_model_task():
    # Fetch training data from the database
    students = Student.objects.all()
    data = []
    for student in students:
        # Assuming we have a method to get student's historical data
        historical_data = student.get_historical_data()
        data.extend(historical_data)
    
    df = pd.DataFrame(data)
    train_model(df)

@shared_task
def predict_student_scores():
    students = Student.objects.all()
    for student in students:
        # Assuming we have a method to get student's current data
        current_data = student.get_current_data()
        for subject, subject_data in current_data.items():
            predicted_score = predict_score(subject_data)
            StudentPrediction.objects.create(
                student=student,
                subject=subject,
                predicted_score=predicted_score
            )

