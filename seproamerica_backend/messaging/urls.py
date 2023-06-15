from django.urls import path
from .views import SendMessageView

urlpatterns = [
    path('sendMessage/', SendMessageView.as_view(), name='sendmessage'),
]