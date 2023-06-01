from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('equipment/', include('equipment.urls')),
    path('services/', include('services.urls')),
    path('cardauth/', include('cardauth.urls')),
    path('notifications/', include('notifications.urls')),
    path('adminC/', TemplateView.as_view(template_name='static/adminC/index.html')),
]
