from django.contrib import admin
from django.urls import path, include
from .views import login, register, profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('prestamos.urls')),
    path('login', login , name = 'login'),
    path('register', register,  name = 'register'),
    path('profile', profile,   name = 'profile')    
]
