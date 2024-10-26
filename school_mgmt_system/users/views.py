from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.views import APIView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .serializers import *
from .models  import *

# Create your views here.

#RETRIEVE ALL USERS
class UserList(APIView):

    #authentication_classes = [SessionAuthentication]
    #permission_classes = ([AllowAny])

    def get(self, request):      
        queryset = User.objects.all()
        serializer = userSerializers(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#REGISTER USER    
class UserRegister(APIView):

    #authentication_classes = [SessionAuthentication]
    #permission_classes = ([AllowAny])
  
    def post(self, request):         
        serializer = RegisterSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user=serializer.data,
            return Response(user, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def signuppage(request):
    return render(request, 'registration.html')



#DETAIL USER   
class UserDetail(APIView):
  
    def get(self,request, pk):
        queryset = User.objects.get(id=pk)
        serializer = userSerializers(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)



#UPDATE USER

class UserUpdate(APIView):

    def patch(self,request, pk):
        queryset = User.objects.get(id=pk)
        serializer = userSerializers(instance=queryset, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_304_NOT_MODIFIED)



#DELETE USER

class UserDelete(APIView):
  
    def get(self, request, pk):
        queryset = User.objects.get(id=pk)
        queryset.delete()
        return Response("User deleted successfully", status=status.HTTP_204_NO_CONTENT)



#USER LOGIN
class Loginview(APIView):

    def post(self, request):
        print(request)
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.POST['email']
        print(email)
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            #print("login successful")
            #return redirect('loginpage')
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Logged in successfully',
            }
            print(response)
            return redirect("http://127.0.0.1:8000/users/")
            return Response(response)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

def loginpage(request):
    return render(request, 'login.html')



#USER LOGOUT

class Logoutview(APIView):

    def get(self, request):
       
        logout(request)
        return redirect("http://127.0.0.1:8000/users/login/")
        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)


def homepage(request):
    return render(request, 'home.html')



# class PasswordChangeView(APIView):
#         model = User

#         def get_object(self, queryset=None):
#             obj = self.request.user
#             return obj

#         def patch(self, request, *args, **kwargs):
#             self.object = self.get_object()
#             #serializer = ChangePasswordSerializer(data=request.data)

#             if serializer.is_valid():
#                 # Check old password
#                 if not self.object.check_password(serializer.data.get("old_password")):
#                     return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
#                 # set_password also hashes the password that the user will get
#                 self.object.set_password(serializer.data.get("new_password"))
#                 self.object.save()


    # def patch(self,request):
    #     user = request.user
    #     response=user.id
    #     serializer = ChangePasswordSerializer(data=request.data)
    #     print(request.data)
    #     print(type(request.data))

    #     oldpass= request.data["old_password"]
    #     print(oldpass)
    #     newpass = request.data["password"]
    #     repeatpass= request.data["password2"]
    #     print(newpass)
    #     print(repeatpass)
    #     print(type(repeatpass))
    #     if serializer.is_valid():
    #         print(serializer.data.get("old_password"))
    #         print("###############################")


class PasswordChangeView(APIView):
    permission_classes = (IsAuthenticated,)
    def patch(self, request):
        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({'success':'Password changed successfully.'}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)


class PasswordReset(APIView):

    def post(self, request):
    
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = User.objects.filter(email=email).first()
        if user:
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_url = reverse("reset-password",kwargs={"encoded_pk": encoded_pk, "token": token})
            reset_link = f"http://127.0.0.1:8000{reset_url}"
            return Response({"message": f"Your password rest link: {reset_link}"},status=status.HTTP_200_OK)
        else:
            return Response({"message": "User doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordComplete(APIView):

    def patch(self, request, *args, **kwargs):

        serializer = ResetPasswordSerializer(data=request.data, context={"kwargs": kwargs})
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Password reset complete"},status=status.HTTP_200_OK)