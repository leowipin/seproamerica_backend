from django.urls import path
from .views import CardView, CurrentCardView

urlpatterns = [
    path('card/', CardView.as_view(), name='card'),
    path('currentCard/', CurrentCardView.as_view(), name='currentcard'),
]