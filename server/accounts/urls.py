from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import RegistrationAPIView, confirm_email_view

app_name = 'accounts'

urlpatterns = [
    path('create-user/', RegistrationAPIView.as_view(), name='user_create'),
    path('confirm-email/<str:confirm_code>/', confirm_email_view, name='confirm_email'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
