from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

api_urls = [
    path('user/', include('user.urls')),
    path('profile/', include('gamecreation.urls')),
    path('ticket/', include('ticket.urls')),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
]
