from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views
from django.views.generic.base import TemplateView
from .views import *
  
urlpatterns = [

#     path('token/', jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
#     path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
#     path('token/verify/', jwt_views.TokenVerifyView.as_view(), name ='token_verify'),

        path('home/', TemplateView.as_view(template_name="home.html"), name='home'),
        path('login/', views.UserLogin.as_view(),name='login'),
        path('signup/', views.UserRegistration.as_view(), name='signup'),
        path('signout/', views.signout, name='signout'),

        path('userlist/', UserList.as_view(), name='userslist'),
        path('delete/', DeleteUser.as_view(), name='delete'),

      
 ]




      

















    # path('user/partialupdate/<int:pk>/',views.partialupdate_user,name='partialupdate_user'),

    
     

#     path('changepassword/<int:pk>/', ChangePasswordView.as_view(), name='change_password'),



#     path('user/detail/<int:pk>/', UserDetail.as_view(), name='user-detail-view'),
 


