from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import ClearanceRequest, ClearanceLog
from .serializers import ClearanceRequestSerializer
from .permissions import CanApproveClearance

class ClearanceRequestViewSet(viewsets.ModelViewSet):
    queryset = ClearanceRequest.objects.all()
    serializer_class = ClearanceRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filter requests based on user's role
        if self.request.user.has_perm('clearance.can_approve_clearance'):
            return ClearanceRequest.objects.all()
        return ClearanceRequest.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                serializer.save(user=self.request.user)
        except ValidationError as e:
            raise ValidationError({"error": str(e)})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, CanApproveClearance])
    def approve(self, request, pk=None):
        try:
            clearance = self.get_object()
            with transaction.atomic():
                clearance.approved = True
                clearance.approver = request.user
                clearance.approved_at = timezone.now()
                clearance.save()
                
                ClearanceLog.objects.create(
                    clearance=clearance,
                    action="approved",
                    performed_by=request.user
                )
                
            return Response(
                {"status": "approved", "approved_at": clearance.approved_at},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to approve clearance: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def access(self, request, pk=None):
        try:
            clearance = self.get_object()
            current_time = timezone.now()
            
            if not clearance.approved:
                return Response(
                    {"error": "Clearance not approved"},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            if not (clearance.start_time <= current_time <= clearance.end_time):
                return Response(
                    {"error": "Clearance not valid at this time"},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            with transaction.atomic():
                ClearanceLog.objects.create(
                    clearance=clearance,
                    action="accessed",
                    performed_by=request.user
                )
                
            return Response(
                {"status": "access granted"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": f"Access check failed: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

