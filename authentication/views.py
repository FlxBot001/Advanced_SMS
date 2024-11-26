from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
     # User registration (sign-up)
    path('register/', RegisterView.as_view(), name='register'),
    
    # JWT token obtain and refresh
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

