from django.contrib import admin
from django.urls import path
from .views import *
from .calviews import *
from .stripe_views import *
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [

    path('token/', jwt_views.TokenObtainPairView.as_view(), name ='token_obtain'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name ='token_verify'),

    path('list/', UserList.as_view(),name='user_list'),
    path('create/', UserRegister.as_view(),name='user_register'),
    path('detail/<int:pk>/', UserDetail.as_view(),name='user_detail'),
    path('update/<int:pk>/', UserUpdate.as_view(),name='user_update'),
    path('delete/<int:pk>/', UserDelete.as_view(),name='user_delete'),

    path('login/', LoginView.as_view(),name='user_login'),
    path('logout/', Logoutview.as_view(),name='user_logout'),

    path('changepassword/',PasswordChangeView.as_view(), name='password_change'),
    #path('resetpassword/',PasswordReset.as_view(),name="request_password_reset"),
    path('celeryresetpassword/',PasswordResetbyCelery.as_view(),name="request_password_reset"),
    path('passwordreset/<str:encoded_pk>/<str:token>/',ResetPasswordComplete.as_view(),name="reset-password-url"),

    path('consumed/addquantity/', AddConsumed.as_view(),name='add_food_consumed'),
    path('consumed/delete/<int:pk>/', ConsumeDelete.as_view(),name='delete_consumed'),
    path('consumed/listview/', ConsumeList.as_view(),name='consumed_listview'),
    path('search/<str:email>/', SearchByemail.as_view(),name='user_register'),
    path('consumed/searchbyday/', SearchConsumedByDay.as_view(),name='food consumed based on day'),
    path('consumed/searchbymonth/', SearchConsumedByMonth.as_view(),name='food consumed based on month'),
    path('consumed/searchbyweek/', SearchConsumedByWeek.as_view(),name='food consumed based on week'),
    path('consumed/search/range/', SearchRange.as_view(),name='food consumed based on date range'),

    #excel
    path('exporttoexcel/', Export.as_view(), name='export_excel_date'),
    path('exporttoexcel/week/', ExportWeek.as_view(), name='export_excel_week'),
    path('exporttoexcel/month/', ExportMonth.as_view(), name='export_excel_month'),
    
    #pdf
    
    path('pdf/date/', Convert_pdf_by_date.as_view(), name='date_pdf'), 
    path('pdf/week/', Convert_pdf_by_week.as_view(), name='week_pdf'), 
    path('pdf/month/', Convert_pdf_by_month.as_view(), name='month_pdf'), 


    #charts

    path('weekwisechart/', weekwisechart_mixin.as_view(), name='week_chart'), 
    path('daywisechart/', daywisechart_mixin.as_view(), name='day_chart'), 
    path('monthwisechart/', monthwisechart_mixin.as_view(), name='monthwisechart'),

    #stripe
    path('choose_plan/', PaymentView.as_view(), name='choose_plan'),
    path('payment_success/', PaymentSuccess.as_view(), name='payment_success'),

    #----TEMPLATE URLS----
    path('loginpage/',loginpage, name='loginpage'),
    path('userloginpage/',userloginpage, name='userloginpage'), #not required
    path('home/',homepage, name='homepage'), #homepage of user
    path('signup/',signuppage, name='signup'),
    path('userlist/',userlistpage, name='userlist'),
    path('home/',userhomepage, name='userhome'),
    path('oldcalc/',calculatecaloriepage, name='userhome'),
    path('calc/',calculatecaloriespage, name='userhome'),
    path('sheet/',sheetpage, name='usersheet'),
    path('passwordchange/',passwordchangepage, name='password_changepage'),
    path('changepassworddone/',passwordchangedonepage, name='password_change_donepage'),
    path('passwordreset/',passwordresetpage, name='password_resetpage'),
    path('resetpasswordsent/',passwordresetsentpage, name='password_reset_completepage'),
    path('resetpassworddone/',passwordresetdonepage, name='password_reset_donepage'),
    path('resetpassword/<str:encoded_pk>/<str:token>/',passwordresetcompletepage,name="reset-password"),
    path('resetpasswordcomplete/',passwordresetcompletepage, name='password_reset_completepage'),
    path('chart/',chart, name='chart'),
    path('navbar/',navbar, name='navbar'),
    path('adminhome/',adminhome, name='admin_homepage'), #home page of admin

    path('daywisechartpage/',daywisechartpage, name='daywisechartpage'),
    path('weekwisechartpage/',weekwisechartpage, name='weekwisechartpage'),
    path('monthwisechartpage/',monthwisechartpage, name='monthwisechartpage'),

    path('payment_success_page/', payment_success_page, name='payment_success'),
    path('choose_plan_page/', choose_plan_page, name='choose_plan'),
    path('payment_cancel/', payment_cancel_page, name='payment_cancel_page'),


    
]














 
    
    

 
