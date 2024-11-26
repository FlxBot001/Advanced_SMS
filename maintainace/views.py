from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import MaintenanceRequest, MaintenanceComment
from .serializers import MaintenanceRequestSerializer, MaintenanceCommentSerializer

class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.all()
    serializer_class = MaintenanceRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        maintenance_request = self.get_object()
        serializer = MaintenanceCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request=maintenance_request, user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

