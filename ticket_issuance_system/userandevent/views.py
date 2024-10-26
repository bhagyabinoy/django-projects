from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from .models  import *
from rest_framework.parsers import JSONParser 
import pdfkit
from django.http import HttpResponse
import datetime
from django.template.loader import render_to_string
from .utils import *
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.mail import send_mail
from ticket_project import settings
from ticketandpayment.models import *
from datetime import datetime
from .mixins import *
import json
from django.utils.crypto import get_random_string
from django.db.models import Value
from django.db.models.functions import Concat
from django.contrib.auth.decorators import login_required

# Create your views here.


##############################################USERS#####################################################
'''RETRIEVE ALL USERS'''
class UserList(APIView):

    permission_classes = [AllowAny]
    
    def get(self, request): 

        queryset = get_all_user_instances()
        serializer = userSerializers(queryset, many=True)
        events = serializer.data
        if events:
            payload = {
                "status": True,
                "message": "All users Retrieved Successfully.",
                "data": events,
                }
            return Response(payload, status=status.HTTP_200_OK)
        else:
            payload = {
                "status": False,
                "message": "No users found.",
                "data": {},
                }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

'''REGISTER  USER'''
class UserRegister(APIView):

    permission_classes = [AllowAny]
  
    def post(self, request):     
        
        serializer = RegisterSerializers(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            event = serializer.data
            payload = {
                "status": True,
                "message": "User Registered Successfully.",
                "data": event,
                }
            return Response(payload, status=status.HTTP_201_CREATED)
        else:
            payload = {
                "status": False,
                "message": "User Creation Failed",
                "data": {},
                }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


''' USER  DETAIL  '''
class UserDetail(APIView):
    
    permission_classes = [AllowAny]

    def get(self,request, pk):

        try:
            queryset = user_detail(pk)
            serializer = userSerializers(queryset, many=False)
            data = serializer.data      
            payload = {
                "status": True,
                "message": "Data retrieved Successfully.",
                "data": data,
                }
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            payload = {
                "status": False,
                "message": "No user was found for the given ID",
                "data": {},
                }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

          
    
''' UPDATE USER'''

class UserUpdate(APIView):

    permission_classes = [AllowAny]

    def patch(self,request, pk):
  
        try:
            queryset = user_detail(pk)
        except User.DoesNotExist:
            payload = {
                "status": False,
                "message": "No user was found for the given ID",
                "data": {},
                }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = userSerializers(instance=queryset, data=request.data, partial=True)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            payload = {
                "status": True,
                "message": "User Updated Successfully.",
                "data": data,
                }
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_304_NOT_MODIFIED)


''' DELETE USER '''

class UserDelete(APIView):

    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    def get(self, request, pk):

        try:
            queryset = user_detail(pk)

        except User.DoesNotExist:
            payload = {
                "status": False,
                "message": "No user was found for the given ID",
                }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        
        queryset.delete()
        payload = {
                "status": False,
                "message": "user deleted successfully",
                }
        return Response(payload, status=status.HTTP_204_NO_CONTENT) 

'''  LOGIN VIEW   '''
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            payload = {
                'status': 'false',
                'message': 'Credentials missing',
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            message = 'User LOGIN SUCCESSFUL' if user.is_admin else 'Admin LOGIN SUCCESSFUL'
            response_data = {
                'status': 'success',
                'message': message,
                'data': {
                    'email': user.email,
                    'user_id': user.id,
                    'user_type': 'admin' if user.is_admin else 'user',
                },
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                'status': 'false',
                'message': 'Invalid Credentials',
            }
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
        
'''   LOG OUT  '''
class Logoutview(APIView):

    def get(self, request):
       
        logout(request)
        return Response({'message': 'Successfully Logged out'}, status=status.HTTP_200_OK)
    

##############################################EVENTS#####################################################

'''RETRIEVE ALL EVENTS'''
class EventList(APIView):

    permission_classes = [AllowAny]
    
    def get(self, request): 
            search_key = request.GET.get("search_key")
            event_start_time = request.GET.get("start_date")
            event_end_time = request.GET.get("end_date")
            print(search_key,event_start_time)
            queryset = get_all_event_instances()
            num_of_events = queryset.count()
            event_start_time = datetime.strptime(event_start_time, "%b %d, %Y %I:%M %p") if event_start_time else None
            event_end_time = datetime.strptime(event_end_time, "%b %d, %Y %I:%M %p") if event_end_time else None
            if event_start_time:
                queryset = queryset.filter(event_start_time__gte=event_start_time)
            if event_end_time:
                queryset = queryset.filter(event_end_time__lte=event_end_time)
            if search_key:
                queryset = queryset.filter(event_name__icontains=search_key)
            serializer = eventSerializers(queryset, many=True)
            events = serializer.data
            
            print(num_of_events)
            if events:
                payload = {
                    "status": True,
                    "message": "All Events Retrieved Successfully.",
                    "data": events,
                    "count": num_of_events
                    }
                return Response(payload, status=status.HTTP_200_OK)
            else:
                payload = {
                    "status": False,
                    "message": "No Events found.",
                    "data": {},
                    }
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)

'''CREATE  EVENT'''
class EventCreate(APIView):

    permission_classes = [AllowAny]
  
    def post(self, request):     

        #if request.user.is_admin:  
        print("Event Create")
        print("request data",request.data)
        serializer = eventSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            event = serializer.data
            payload = {
                "status": True,
                "message": "Event Created Successfully.",
                "data": event,
                }
            return Response(payload, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            payload = {
                "status": False,
                "message": "Event Creation Failed",
                "data": {},
                }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     payload = {
        #             "status": False,
        #             "message": "Only Admin is allowed",
        #             "data": {},
        #             }
        #     return Response(payload, status=status.HTTP_400_BAD_REQUEST)   


''' EVENT   DETAIL  '''
class EventDetail(APIView):
    
    permission_classes = [AllowAny]

    def get(self,request, pk):

        try:
            queryset = event_detail(pk)
            serializer = eventSerializers(queryset, many=False)
            data = serializer.data      
            payload = {
                "status": True,
                "message": "Data retrieved Successfully.",
                "data": data,
                }
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            payload = {
                "status": False,
                "message": "No event was found for the given ID",
                "data": {},
                }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

          
    
''' UPDATE EVENT '''

class EventUpdate(APIView):

    permission_classes = [AllowAny]

    def patch(self,request, pk):

        try:
            queryset = event_detail(pk)
        except Event.DoesNotExist:
            payload = {
                "status": False,
                "message": "No event was found for the given ID",
                "data": {},
                }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = eventSerializers(instance=queryset, data=request.data, partial=True)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            payload = {
                "status": True,
                "message": "Event Updated Successfully.",
                "data": data,
                }
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_304_NOT_MODIFIED)
            


''' DELETE EVENT  '''

class EventDelete(APIView):

    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    def get(self, request, pk):
        
        if request.user.is_admin:
            try:
                queryset = event_detail(pk)

            except Event.DoesNotExist:
                payload = {
                    "status": False,
                    "message": "No event was found for the given ID",
                    }
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)
            
            queryset.delete()
            payload = {
                    "status": False,
                    "message": "Event deleted successfully",
                    }
            return Response(payload, status=status.HTTP_204_NO_CONTENT) 
        else:
            payload = {
                    "status": False,
                    "message": "Only Admin is allowed",
                    }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)  
        

############################################## PROFILE #####################################################
      

class ProfileDetail(APIView):
    
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:

            user = get_object_or_404(User, id=pk)
            profile = get_object_or_404(Profile, user=user)
            serializer = profileSerializers(profile)

            payload = {
                "status": True,
                "message": "Data retrieved successfully.",
                "data": serializer.data,
            }

            return Response(payload, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            payload = {
                "status": False,
                "message": "No user was found for the given ID",
                "data": {},
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        except Profile.DoesNotExist:
            payload = {
                "status": False,
                "message": "No profile was found for the given user ID",
                "data": {},
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

          
''' UPDATE Profile'''

class ProfileUpdate(APIView):

    permission_classes = [AllowAny]

    def patch(self,request, pk):
        try:

            user = get_object_or_404(User, id=pk)
            print(user)
            profile = get_object_or_404(Profile, user=user)
            print(profile)
            serializer = profileSerializers(instance=profile, data=request.data, partial=True)
            print(request.data)
            if serializer.is_valid():
                print("valid")
                serializer.save()
                data = serializer.data

                payload = {
                    "status": True,
                    "message": "Profile updated successfully.",
                    "data": data,
                }
                return Response(payload, status=status.HTTP_200_OK)
            else:
                print(serializer.errors)
                payload = {
                    "status": False,
                    "message": "Profile updated sfailed",
                    "data":serializer.errors,
                }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            payload = {
                "status": False,
                "message": "No user was found for the given ID",
                "data": {},
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        except Profile.DoesNotExist:
            payload = {
                "status": False,
                "message": "No profile was found for the given user ID",
                "data": {},
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


''' DELETE Profile '''

class ProfileDelete(APIView):

    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    def get(self, request, pk):

        try:
            user = get_object_or_404(User, id=pk)
            print(user)
            profile = get_object_or_404(Profile, user=user)
            profile.delete()
            payload = {
                    "status": False,
                    "message": "Profile deleted successfully",
                    }
            return Response(payload, status=status.HTTP_204_NO_CONTENT) 
        except User.DoesNotExist:
            payload = {
                "status": False,
                "message": "No user was found for the given ID",
                "data": {},
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        except Profile.DoesNotExist:
            payload = {
                "status": False,
                "message": "No profile was found for the given user ID",
                "data": {},
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


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

class ResetPasswordComplete(APIView):

    permission_classes = ([AllowAny])

    def get(self, request, *args, **kwargs):
        return render(request, 'password_reset_done.html')

    def patch(self, request, *args, **kwargs):

        serializer = ResetPasswordSerializer(data=request.data, context={"kwargs": kwargs})
        if serializer.is_valid(raise_exception=True):
            return Response({"message": "Password reset complete"},status=status.HTTP_200_OK)



''' api to set price to an event '''
class SetPricetoEvent(APIView):

    permission_classes = ([AllowAny])

    def post(self, request):
        
        event_id = request.data.get('event_id','')
        eventpricing_id = request.data.get('event_pricing_id','')
        print(event_id, eventpricing_id)
        if not event_id or not eventpricing_id:
            payload = {
                "status": False,
                "message": "Both event_id and event_pricing_id are required.",
                }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            payload = {
                "status": False,
                "message": "Event not found.",
                }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        try:
            pricing_instance = Pricing.objects.get(id=eventpricing_id)
        except Pricing.DoesNotExist:
            payload = {
                "status": False,
                "message": "Pricing not found.",
                }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        event.pricing.add(pricing_instance)
        payload = {
                "status": True,
                "message": "Pricing mapped to event successfully..",
                }
        return Response(payload, status=status.HTTP_200_OK)


''' api to book an event'''

class BookanEvent(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.data,"data received-----------")
        event_id = request.data.get('event_id','')
        user_id = request.data.get('user_id','')
        seat_booked = request.data.get('seat_booked')
        print("seat_booked--------------------", seat_booked)
        print("event_id--------------------",event_id)

        if seat_booked:
            event = get_object_or_404(Event, id=event_id)
            total_seats = event.total_seats
            booked_seats = event.booked_seats or []
            print(booked_seats, "----------------booked_seats----------------")
            print(type(booked_seats))

            for seat_number in seat_booked:
                if seat_number in booked_seats or seat_number > total_seats:
                    payload = {
                        "status": False,
                        "data": {},
                        "message": f"Seat {seat_number} is already booked or not available.",
                    }
                    return Response(payload, status=status.HTTP_400_BAD_REQUEST)

            for seat_number in seat_booked:
                booked_seats.append(seat_number)
            event.booked_seats = booked_seats
            event.save()

            event_booking_data = {
                'event': event_id,
                'user': user_id,
                'seats_booked': seat_booked,
            }

            serializer = eventbookingSerializers(data=event_booking_data)
            if serializer.is_valid():
                serializer.save()
                payload = {
                    "status": True,
                    "data": serializer.data,
                    "message": "Event Booked successfully..",
                }
                return Response(payload, status=status.HTTP_200_OK)
            payload = {
                "status": False,
                "data": serializer.errors,
                "message": "Booking unsuccessful.",
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

''' api to list eventa by user'''
class ListEventsBookedByuser(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.GET.get('user_id', '')
        if user_id:
            print("user_id-----------------", user_id)
            event_booking_data = EventBookings.objects.filter(user_id=user_id)
            print("event booking data", event_booking_data)
            serializer = eventbookingdisplaySerializers(event_booking_data, many=True)
            print(serializer.data)
            payload = {
                "status": True,
                "data": serializer.data,
                "message": "Data retrieved successfully..",
            }
            return Response(payload, status=status.HTTP_200_OK)

        payload = {
            "status": False,
            "data": {},
            "message": "Failed to retrieve data",
        }
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)



''' api to list eventa by user'''
class ListBookingbasedonEvent(APIView):

    permission_classes = ([AllowAny])

    def get(self, request):
        event_id = request.GET.get('event_id', '')
        if event_id:
            print("user_id-----------------", event_id)
            event_booking_data = EventBookings.objects.filter(event_id=event_id)
            print("event booking data", event_booking_data)
            serializer = eventbookingdisplaySerializers(event_booking_data, many=True)
            print(serializer.data)
            payload = {
                "status": True,
                "data": serializer.data,
                "message": "Data retrieved successfully..",
            }
            return Response(payload, status=status.HTTP_200_OK)

        payload = {
            "status": False,
            "data": {},
            "message": "Failed to retrieve data",
        }
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        

''' api to get seating availability '''
class EventSeatAvailability(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        event_id = request.GET.get('event_id', '')

        if event_id:
            try:
                event = Event.objects.get(id=event_id)
            except Event.DoesNotExist:
                payload = {
                    "status": False,
                    "data": {},
                    "message": "Event not found.",
                }
                return Response(payload, status=status.HTTP_404_NOT_FOUND)

            serializer = EventSeatStatusSerializer(event)
            payload = {
                "status": True,
                "data": serializer.data,
                "message": "Data retrieved successfully.",
            }
            return Response(payload, status=status.HTTP_200_OK)

        payload = {
            "status": False,
            "data": {},
            "message": "Invalid event_id.",
        }
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)
    

''' api to get pre payment information'''
class PrePaymentInfo(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        print(request.data,"----------------------------------")
        user_id = request.query_params.get('user_id')
        booking_id = request.query_params.get('booking_id')
        print(user_id, booking_id)
        if not user_id or not booking_id:
            payload = {
                "status": False,
                "message": "Both user_id and booking_id are required.",
                }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user = User.objects.get(id=user_id)
                print(user)
            except User.DoesNotExist:
                response_data = {
                    'status': 'false',
                    'message': 'User does not exist',
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            try:
                booking = EventBookings.objects.get(id=booking_id)
                print(booking)
            except EventBookings.DoesNotExist:
                response_data = {
                    'status': 'false',
                    'message': 'Event Bookings does not exist',
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            if booking:
                serializer = eventbookingdisplaySerializers(booking)
                data = serializer.data
                event_name = data.get("event_name",'')
                seats_booked = data.get('seats_booked','')
                event_start_time = data.get('event_start_time'),
                event_end_time = data.get('event_end_time')
                quantity = len(seats_booked)
                pricing = data.get('pricing','')
                pricing_dict = pricing[0]
                pricing_table_id = pricing_dict.get('id','')
                if pricing_table_id:
                    pricing_query = Pricing.objects.get(id=pricing_table_id)
                    unit_amount = pricing_query.unit_amount
                    total_amount = unit_amount*quantity
                    data = {
                            'event_name':event_name,
                            'seats_booked':seats_booked,
                            'unit_amount':unit_amount,
                            'total_amount':total_amount,
                            'event_start_time':event_start_time,
                            'event_end_time':event_end_time
                            }
                    response_data = {
                        'status': 'True',
                        'data': data,
                        'message': 'Data Fetched successfully',
                        }
                    return Response(response_data, status=status.HTTP_200_OK)
        response_data = {
                        'status': 'False',
                        'data': data,
                        'message': 'Data Fetching Failed',
                        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)                


class ListingChatRooms(APIView):

    def get(self, request):
        try:

            room_dict = Message.objects.order_by().annotate(
                    room_sender=Concat('room_name', Value('_'), 'sender', output_field=models.CharField())
                ).values('room_name', 'sender').distinct()

            print(room_dict)
            response_data = {
                'status': 'True',
                'data': room_dict,
                'message': 'Data Fetched successfully',
                }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                            'status': 'False',
                            'data': {},
                            'message': 'Data Fetching Failed',
                            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    
''' TEMPLATE URLS  '''
def userpage(request):
    return render(request, 'user.html')

def eventpage(request):
    return render(request, 'event.html')

def addpriceeventpage(request):
    return render(request, 'add_price_event.html')

def eventdetailpage(request):
    return render(request, 'event_detail.html')

def signuppage(request):
    return render(request, 'signup.html')

def loginpage(request):
    return render(request, 'login.html')

def homepage(request):
    return render(request, 'home.html')

def adminhomepage(request):
    if request.user.is_authenticated and request.user.is_admin:
        print("----------user---------------",request.user)
        return render(request, 'adminhome.html')
    return render(request, 'login.html')
    

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

def addeventpage(request):
    return render(request, 'addevent.html')

def admineventpage(request):
    return render(request, 'admin_event.html')

def profilepage(request):
    return render(request, 'profile.html')

def bookingpage(request):
    return render(request, 'booking.html')

def paymentsuccesspage(request):
    return render(request, 'payment_success.html')

def paymentcancelpage(request):
    return render(request, 'payment_cancel.html')


def adminchatroompage(request):
    if request.user.is_authenticated and request.user.is_admin:
    # print("----------user---------------",request.user)
    # admin = request.user.is_admin
    # print(admin)
    # if admin:
        return render(request, 'admin_rooms.html')
    else:
        return render(request, 'login.html')


def chatpageforuser(request):
    print(request.user,"-------------user------------------")
    if request.user.is_authenticated:
        user = request.user
        try:
            msgobj = Message.objects.filter(user=user).first()
            print(msgobj,"-------------")
            if msgobj:
                room_name = msgobj.room_name
            else:
                room_name = get_random_string(length=8)
                print("Room name------------------",room_name)
        except Message.DoesNotExist:
            print("no room availble")
            room_name = get_random_string(length=8)
            print("Room name------------------",room_name)
        return render(request, 'chatting.html', {'room_name': room_name})
    else:
        return render(request, 'login.html')

def chatpageforadmin(request, slug):
    return render(request, 'chatting.html', {'room_name': slug})

def profileupdatepage(request):
    return render(request, 'profileupdate.html')