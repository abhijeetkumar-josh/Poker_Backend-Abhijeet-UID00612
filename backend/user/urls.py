from django.urls import path
from user.views import RegisterView,LoginView,VerifyEmailView,UserSearchView,get_public_key

app_name = 'user'

urlpatterns = [
    path('signup/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('verify-email/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('search', UserSearchView.as_view(), name='search'),
    path('publickey', get_public_key, name='publickey')
]
