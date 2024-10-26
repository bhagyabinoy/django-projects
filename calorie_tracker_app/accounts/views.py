from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.mail import send_mail
from .serializers import *
from .models  import *
import logging
import datetime
from .utils import accounts_utils,logs_utils
from accounts.tasks import send_password_reset_email
from rest_framework_simplejwt.tokens import RefreshToken


##################################################################################################################################


logger = logging.getLogger(__name__)


#RETRIEVE ALL USERS
class UserList(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request): 
        
        if request.user.is_staff:

            #queryset = User.objects.all().order_by('id')
            queryset = accounts_utils.get_all_user_instances()
            serializer = userSerializers(queryset, many=True)
            logger.warning('User page was accessed at '+str(datetime.datetime.now())+' hours!')
            return Response(serializer.data, status=status.HTTP_200_OK)     
        else:
            return Response("Only Admin is allowed view list of users", status=status.HTTP_400_BAD_REQUEST)

##################################################################################################################################

#REGISTER USER    
class UserRegister(APIView):

    permission_classes = [AllowAny]
  
    def post(self, request):         
        serializer = RegisterSerializers(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            user=serializer.data
            print(user)
            return Response(user, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

##################################################################################################################################

#DETAIL USER   
class UserDetail(APIView):
    
    permission_classes = [AllowAny]
 

    def get(self,request, pk):
            
        try:
            queryset = accounts_utils.user_detail(pk)
        except User.DoesNotExist:
            return Response("No User was found for the given ID", status=status.HTTP_404_NOT_FOUND)
        serializer = userSerializers(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
  

##################################################################################################################################

#UPDATE USER

class UserUpdate(APIView):

    permission_classes = [AllowAny]

    def patch(self,request, pk):
        try:
            queryset = accounts_utils.user_detail(pk)
        except User.DoesNotExist:
            return Response("No User was found for the given ID", status=status.HTTP_404_NOT_FOUND)

        serializer = userSerializers(instance=queryset, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_304_NOT_MODIFIED)

##################################################################################################################################

#DELETE USER

class UserDelete(APIView):

    permission_classes = [AllowAny]
  
    def get(self, request, pk):

        try:
            queryset = accounts_utils.user_detail(pk)
        except User.DoesNotExist:
            return Response("No User was found for the given ID", status=status.HTTP_404_NOT_FOUND)
        queryset.delete()
        return Response("User deleted successfully", status=status.HTTP_200_OK)
  

##################################################################################################################################

#LOGIN VIEW 
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            response_data = {
                'status': 'false',
                'message': 'Credentials missing',
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            message = 'User LOGIN SUCCESSFUL' if user.is_staff else 'Admin LOGIN SUCCESSFUL'
            response_data = {
                'status': 'success',
                'message': message,
                'data': {
                    'email': user.email,
                    'user_id': user.id,
                    'user_type': 'admin' if user.is_staff else 'user',
                },
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                'status': 'false',
                'message': 'Invalid Credentials',
            }
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

##################################################################################################################################

#USER LOGOUT

class Logoutview(APIView):

    def get(self, request):
       
        logout(request)
        return Response({'message': 'Successfully Logged out'}, status=status.HTTP_200_OK)

##################################################################################################################################

class PasswordChangeView(APIView):

    permission_classes = [IsAuthenticated]
    def patch(self, request):

        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        print(request.data)
        if serializer.is_valid(raise_exception=ValueError):
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({'success':'Password changed successfully.'}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)

##################################################################################################################################

class PasswordReset(APIView):

    permission_classes = ([AllowAny])

    def post(self, request):
    
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = User.objects.filter(email=email).first()

        if user:

            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_url = reverse("reset-password-url",kwargs={"encoded_pk": encoded_pk, "token": token})
            reset_link = f"http://127.0.0.1:8000{reset_url}"

            #sending mail
            subject = 'Password reset link'
            message = f"You are receiving this email because you requested a password reset for your user account at 127.0.0.1:8000. Your password rest link is: {reset_link} \nThanks for using our site! \nThe 127.0.0.1:8000 team"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail( subject, message, email_from, recipient_list )
            return Response({"message": f"Your password rest link: {reset_link}"},status=status.HTTP_200_OK)
        
        else:
            return Response({"message": f"Can't send E-mail. \nThere is no user registered with this email address"}, status=status.HTTP_400_BAD_REQUEST)

##################################################################################################################################

class ResetPasswordComplete(APIView):

    permission_classes = ([AllowAny])

    def get(self, request, *args, **kwargs):
        return render(request, 'password_reset_done.html')

    def patch(self, request, *args, **kwargs):

        serializer = ResetPasswordSerializer(data=request.data, context={"kwargs": kwargs})
        if serializer.is_valid(raise_exception=True):
            return Response({"message": "Password reset complete"},status=status.HTTP_200_OK)


##################################################################################################################################
class SearchByemail(APIView):

    permission_classes = ([AllowAny])

    def get(self, request,email):
    
        user = User.objects.filter(email=email).values_list('id')
        if user:
            id= user
            return Response(user,status=status.HTTP_200_OK)


class PasswordResetbyCelery(APIView):

    permission_classes = ([AllowAny])

    def post(self, request):
    
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = User.objects.filter(email=email).first()

        if user:

            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_url = reverse("reset-password-url",kwargs={"encoded_pk": encoded_pk, "token": token})
            reset_link = f"http://127.0.0.1:8000{reset_url}"
            recipient_list = [email]
            print(recipient_list)
            send_password_reset_email.delay(recipient_list, reset_link)
            return Response({"message": f"Your password rest link: {reset_link}"},status=status.HTTP_200_OK)
        
        else:
            return Response({"message": f"Can't send E-mail. \nThere is no user registered with this email address"}, status=status.HTTP_400_BAD_REQUEST)


#TEMPLATE VIEWS

def signuppage(request):
    return render(request, 'signup.html')

def loginpage(request):
    return render(request, 'login.html')

def userloginpage(request):
    return render(request, 'userlogin.html')

def homepage(request):
    return render(request, 'home.html')

def userlistpage(request):
    return render(request, 'userlist.html')

def userhomepage(request):
    return render(request, 'consume.html')

def calculatecaloriepage(request):
    return render(request, 'old_consume.html')

def calculatecaloriespage(request):
    return render(request, 'consume.html')

def profilepage(request):
    return render(request, 'profile.html')

def sheetpage(request):
    return render(request, 'sheet.html')

def passwordchangepage(request):
    return render(request, 'passwordchange.html')

def passwordchangedonepage(request):
    return render(request, 'passwordchangedone.html')

def passwordresetpage(request):
    return render(request, 'password_reset.html')

def passwordresetsentpage(request):
    return render(request, 'password_reset_sent.html')

def passwordresetdonepage(request):
    return render(request, 'password_reset_done.html')

def passwordresetcompletepage(request):
    return render(request, 'password_reset_complete.html')

def chart(request):
    return render(request, 'chart.html')

def navbar(request):
    return render(request, 'navbar.html')

def adminhome(request):
    return render(request, 'admin_homepage.html')
##################################################################################################################################


