from django.urls import path
from users.views import *

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('clientSignin/', ClientSignInView.as_view(), name='clientsignin'),
    path('adminSignin/', AdminSignInView.as_view(), name='adminsignin'),
    path('operationalSignin/', OperationalSignInView.as_view(), name='operationalsignin'),
    path('verification/<str:token>', VerifyEmail.as_view(), name='verification'),
    path('group/', GroupView.as_view(), name='group'),
    path('adminCreate/', AdminCreateView.as_view(), name='admincreate'),
    path('operationalCreate/', OperationalCreateView.as_view(), name='operationalcreate'),
]