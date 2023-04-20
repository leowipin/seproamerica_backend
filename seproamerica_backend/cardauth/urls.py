from django.urls import path
from .views import CardView

urlpatterns = [
    path('card/', CardView.as_view(), name='card'),
]