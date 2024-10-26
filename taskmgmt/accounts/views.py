from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from django.contrib.auth import authenticate, login, logout
from .serializers import *
from django.views.generic import View
from django.contrib import messages



####################################################################################################################################################################


#USER REGISTRATION

class UserRegistration(View):

    def get(self, request):
        return render(request, template_name='signup.html')

    def post(self, request):
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            re_password = request.POST.get('re_password')

            print(first_name,last_name,username,email )

            if(password != re_password):
                messages.add_message(request, messages.INFO, 'passwords donot match.')
            else:
                try:
                    User.objects.get(username = request.POST['username'])
                    return render (request,'signup.html', {'error':'Username is already taken!'})
                except User.DoesNotExist:
                    user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email, password=password)
                    print("success")
                    return redirect('login')


####################################################################################################################################################################


#USER LOGIN

class UserLogin(View):

    def get(self, request):
        return render(request, template_name='login.html')

    def post(self, request):
        user = authenticate(username=request.POST['username'],password = request.POST['password'])
        if user is not None:
            login(request,user)
            return render(request, template_name='home.html')
        else:
            print("error")
            return JsonResponse({"status":"invalid credentials"})
   

####################################################################################################################################################################


#USER LOGOUT 
    
def signout(request):
    
    logout(request)
    return redirect('login')


####################################################################################################################################################################


#RETRIEVE ALL USERS

class UserList(APIView):
    renderer_classes = [JSONRenderer,TemplateHTMLRenderer]
    template_name = 'userlist.html'
    def get(self, request):
        items = User.objects.order_by('id')
        serializer = userSerializer(items, many =True)
        data=serializer.data
        return Response({'data': data})
       
        
####################################################################################################################################################################


#DELETE USER

class DeleteUser(APIView):
        
    def get(self, request):
        
        delete_id = request.GET.get('delete_id')
        User.objects.get(id=delete_id).delete()
        return JsonResponse({"status":"1"})
       

####################################################################################################################################################################





####################################################################################################################################################################




####################################################################################################################################################################

