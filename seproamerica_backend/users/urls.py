from django.urls import path
from users.views import *

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
]