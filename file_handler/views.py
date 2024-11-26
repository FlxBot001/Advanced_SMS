from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import File
from .serializers import FileSerializer

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        file = self.get_object()
        # Add file processing logic here
        file.processed = True
        file.save()
        return Response({'status': 'file processed'})

