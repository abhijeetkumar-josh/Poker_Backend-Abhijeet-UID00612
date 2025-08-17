from django.urls import path
from user.views import RegisterView,LoginView,VerifyEmailView,EditView

app_name = 'user'

urlpatterns = [
    path('signup/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('edit/', EditView.as_view(), name="edit"),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
]
