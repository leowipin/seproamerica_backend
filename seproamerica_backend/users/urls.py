from django.urls import path
from users.views import *

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verification/<str:token>', VerifyEmail.as_view(), name='verification'),
    path('group/', GroupView.as_view(), name='group'),
    path('adminCreate/', AdminCreateView.as_view(), name='admincreate'),
]