from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [

    #user urls
    path('create/', UserRegister.as_view(),name='user_register'),
    path('list/', UserList.as_view(),name='user_list'),
    path('detail/<int:pk>/', UserDetail.as_view(),name='user_detail'),
    path('update/<int:pk>/', UserUpdate.as_view(),name='user_update'),
    path('delete/<int:pk>/', UserDelete.as_view(),name='user_delete'),

    path('login/', LoginView.as_view(),name='user_login'),
    path('logout/', Logoutview.as_view(),name='user_logout'),
    #path('loginpage/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    path('profile/detail/<int:pk>/', ProfileDetail.as_view(),name='profile_detail'),
    path('profile/update/<int:pk>/', ProfileUpdate.as_view(),name='profile_update'),
    path('profile/delete/<int:pk>/', ProfileDelete.as_view(),name='profile_delete'),
    
    path('changepassword/',PasswordChangeView.as_view(), name='password_change'),
    path('resetpassword/',PasswordReset.as_view(),name="request_password_reset"),
    path('passwordreset/<str:encoded_pk>/<str:token>/',ResetPasswordComplete.as_view(),name="reset-password-url"),

    path('passwordchange/',passwordchangepage, name='password_changepage'),
    path('changepassworddone/',passwordchangedonepage, name='password_change_donepage'),
    path('passwordreset/',passwordresetpage, name='password_resetpage'),
    path('resetpasswordsent/',passwordresetsentpage, name='password_reset_completepage'),
    path('resetpassworddone/',passwordresetdonepage, name='password_reset_donepage'),
    path('resetpassword/<str:encoded_pk>/<str:token>/',passwordresetcompletepage,name="reset-password"),
    path('resetpasswordcomplete/',passwordresetcompletepage, name='password_reset_completepage'),

    #event urls
    path('event/list/', EventList.as_view(),name='event_list'),
    path('event/create/', EventCreate.as_view(),name='event_create'),
    path('event/detail/<int:pk>/', EventDetail.as_view(),name='event_detail'),
    path('event/update/<int:pk>/', EventUpdate.as_view(),name='event_update'),
    path('event/delete/<int:pk>/', EventDelete.as_view(),name='event_delete'),
    path('event/setprice/', SetPricetoEvent.as_view(),name='SetPricetoEvent'),
    path('event/book/', BookanEvent.as_view(),name='bookanevent'),
    path('event/listbyuser/', ListEventsBookedByuser.as_view(),name='event_list_user'),
    path('event/listbyevent/', ListBookingbasedonEvent.as_view(),name='event_list'),
    path('event/seat/', EventSeatAvailability.as_view(),name='event_seatavailabilty'),
    path('event/payment/', PrePaymentInfo.as_view(),name='event_payment'),
    path('listingchatrooms/',ListingChatRooms.as_view(), name='listingchatrooms'),

    #template 
    path('user/',userpage, name='userpage'),
    
    path('addeventpage/',addeventpage, name='addeventpage'),
    path('admineventpage/',admineventpage, name='admineventpage'),
    path('eventdetailpage/',eventdetailpage, name='event_detail_page'),
    path('addpriceeventpage/',addpriceeventpage, name='addpriceeventpage'),
    path('loginpage/',loginpage, name='loginpage'),
    path('signup/',signuppage, name='signup'),
    path('ticket/adminlogin/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('',homepage, name='user_homepage'),
    path('adminhome/',adminhomepage, name='admin_homepage'),
    
    path('bookingpage/',bookingpage, name='bookingpage'),
    
    path('payment_success_page/',paymentsuccesspage, name='payment_success_page'),
    path('payment_cancel_page/',paymentcancelpage, name='payment_cancel_page'),

    path('chat/',chatpageforuser, name='chat_page_user'),
    path('chatadmin/<slug:slug>/',chatpageforadmin, name='chat_page_admin'),
    path('adminrooms/',adminchatroompage, name='chat_page_admin'),

    path('profile/',profilepage, name='profile_page'),
    path('profileupdate/',profileupdatepage, name='profile_update_page'),
]