from celery import shared_task
from celery.schedules import crontab
from django.conf import settings
from django.core.cache import cache
import whisper
import numpy as np
import torch
from datetime import timedelta

# ... existing tasks ...

@shared_task
def schedule_model_training():
    """
    Scheduled task to retrain the model if there's new data
    Includes cache checking to avoid unnecessary training
    """
    last_training_key = 'last_model_training_timestamp'
    last_training = cache.get(last_training_key)
    
    if last_training:
        # Check if any new records since last training
        new_records = AcademicRecord.objects.filter(
            created_at__gt=last_training
        ).exists()
        
        if not new_records:
            return "No new data to train on"
    
    # Proceed with training
    training_result = train_performance_model.delay()
    
    if training_result.successful():
        cache.set(last_training_key, timezone.now(), timeout=None)
        return "Model training completed successfully"
    return "Model training failed"


class VoiceInputProcessor:
    def __init__(self):
        self.model = whisper.load_model("base")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    def transcribe_audio(self, audio_file):
        """Transcribe audio file to text"""
        try:
            result = self.model.transcribe(audio_file)
            return result["text"]
        except Exception as e:
            return f"Error transcribing audio: {str(e)}"

@shared_task
def process_voice_input(audio_file_path):
    """Process voice input and convert to structured data"""
    processor = VoiceInputProcessor()
    text = processor.transcribe_audio(audio_file_path)
    
    # Parse the transcribed text for student data
    parsed_data = parse_voice_command(text)
    
    if parsed_data:
        create_or_update_student_record.delay(parsed_data)
        return "Voice input processed successfully"
    return "Could not parse voice command"

def parse_voice_command(text):
    """
    Parse voice commands into structured data
    Example: "Add student John Doe ID 12345 Math score 85"
    """
    import re
    
    patterns = {
        'add_student': r'add student[:]?\s+(?P<name>[\w\s]+)[\s,]+ID[:]?\s+(?P<id>\d+)[\s,]+(?P<subject>\w+)\s+score[:]?\s+(?P<score>\d+)',
        'update_score': r'update student[:]?\s+(?P<id>\d+)[\s,]+(?P<subject>\w+)\s+score[:]?\s+(?P<score>\d+)',
    }
    
    for command_type, pattern in patterns.items():
        match = re.match(pattern, text.lower())
        if match:
            data = match.groupdict()
            data['command_type'] = command_type
            return data
    
    return None

@shared_task
def create_or_update_student_record(parsed_data):
    """Create or update student records based on voice input"""
    try:
        if parsed_data['command_type'] == 'add_student':
            student = Student.objects.create(
                student_id=parsed_data['id'],
                name=parsed_data['name']
            )
            AcademicRecord.objects.create(
                student=student,
                subject=parsed_data['subject'],
                score=float(parsed_data['score'])
            )
            
        elif parsed_data['command_type'] == 'update_score':
            student = Student.objects.get(student_id=parsed_data['id'])
            AcademicRecord.objects.create(
                student=student,
                subject=parsed_data['subject'],
                score=float(parsed_data['score'])
            )
            
        return True
    except Exception as e:
        return f"Error processing record: {str(e)}" 