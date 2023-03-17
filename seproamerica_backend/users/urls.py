from django.urls import path
from users.views import *

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('clientSignin/', ClientSignInView.as_view(), name='clientsignin'),
    path('client/', ClientView.as_view(), name='client-detail'),
    path('clientNames/', ClientNamesView.as_view(), name='clientnamew'),
    path('clientList/', ClientListView.as_view(), name='clientlist'),
    path('adminSignin/', AdminSignInView.as_view(), name='adminsignin'),
    path('adminStaff/', AdminView.as_view(), name='adminstaff'),
    path('adminList/', AdminListView.as_view(), name='adminlist'),
    path('adminClient/', AdminClientView.as_view(), name='adminclient'),
    path('operationalSignin/', OperationalSignInView.as_view(), name='operationalsignin'),
    path('operationalStaff/', OperationalView.as_view(), name='operationalstaff'),
    path('operationalList/', OperationalListView.as_view(), name='operationallist'),
    path('verification/<str:token>', VerifyEmail.as_view(), name='verification'),
    path('group/', GroupView.as_view(), name='group'),
    path('getPermissions/', PermissionsView.as_view(), name='getpermissions'),
    path('adminGroupList/', AdminGroupList.as_view(), name='admingrouplist'),
    path('operationalGroupList/', OperationalGroupList.as_view(), name='operationalgrouplist'), #endpoint not used yet
    path('groupList/', GroupListView.as_view(), name='grouplist'),
    path('passwordReset/', PasswordReset.as_view(), name='passwordreset'),
    path('changePassword/', ChangePassword.as_view(), name='changepassword'),
    path('changeEmail/', ChangeEmail.as_view(), name='changeemail'),
    path('newEmailVerification/<str:token>', VerifyNewEmail.as_view(), name='newemailverification'),
    path('changeNewPassword/', ChangeNewPassword.as_view(), name='changenewpassword'),
    path('newPasswordVerification/<str:token>', VerifyNewPassword.as_view(), name='newpasswordverification'),
    path('phoneAccount/', PhoneAccountView.as_view(), name='phoneaccount'),
    path('phoneAccountList/', PhoneAccountList.as_view(), name='phoneaccountlist'),
]