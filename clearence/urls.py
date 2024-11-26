from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'requests', views.ClearanceRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', views.ClearanceStatsView.as_view(), name='clearance-stats'),
    path('bulk-approve/', views.BulkApproveView.as_view(), name='bulk-approve'),
] 