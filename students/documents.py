from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Student

@registry.register_document
class StudentDocument(Document):
    user = fields.ObjectField(properties={
        'username': fields.TextField(),
        'first_name': fields.TextField(),
        'last_name': fields.TextField(),
    })

    class Index:
        name = 'students'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Student
        fields = [
            'student_id',
            'grade',
        ]

