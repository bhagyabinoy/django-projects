from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    path('list/', UserList.as_view(),name='user-list'),
    path('create/', UserRegister.as_view(),name='user-register'),
    path('detail/<int:pk>/', UserDetail.as_view(),name='user-detail'),
    path('update/<int:pk>/', UserUpdate.as_view(),name='user-update'),
    path('delete/<int:pk>/', UserDelete.as_view(),name='user-delete'),

    path('loginview/', Loginview.as_view(),name='user_login'),
    path('login/',loginpage, name='loginview'),
    path('signup/',signuppage, name='signupview'),
    path('logout/', Logoutview.as_view(),name='user-logout'),
    # path('changepassword/', ChangePasswordView.as_view(),name='change-password'),

    path('',homepage, name='home_view'),
    path('passwordchange/',PasswordChangeView.as_view(), name='password_change'),

    path('resetpassword/',PasswordReset.as_view(),name="request-password-reset"),

    path("passwordreset/<str:encoded_pk>/<str:token>/",ResetPasswordComplete.as_view(),name="reset-password"),

    #path('accounts/change-password', ChangePasswordView.as_view(), name='register'),
    #path('changepassword/', PasswordChangeView.as_view()),
    #path('changepassword/done/', auth_views.PasswordChangeDoneView.as_view(template_name="passwordchangedone.html"),name='password_change_done'),
    #path('resetpassword/',auth_views.PasswordResetView.as_view(template_name="password_reset.html"),name='password_reset'),  
    #path('resetpassworddone/',auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),name='password_reset_done'),  
    #path('resetpasswordconfrim/<uidb64>/<token>/',auth_views. PasswordResetConfirmView.as_view(),name='password_reset_confirm'),  
    #path('resetpasswordcomplete/',auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),name='password_reset_complete'),    
]
