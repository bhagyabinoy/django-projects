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
import stripe
import datetime
from ticket_project import settings
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from userandevent.serializers import *
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives


# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY
class CreatePricing(APIView):

    def post(self,request):
        try:
            name = request.data.get('name')
            event_type = request.data.get('event_type')
            description = request.data.get('description')

            product = stripe.Product.create(
                name=name,
                type=event_type,
                description=description
            )
            pricing_obj = Pricing.objects.create(
                name=product.name,
                description=product.description,
                eventpricing_id = product.id
            )
            print(pricing_obj)
            response_data = {
                    'status': 'true',
                    'data': {
                        'eventpricing_id': product.id,
                        'pricing_name': product.name,
                        'pricing_description': product.description,
                    },
                    'message': 'Pricing created successfully',
                }
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            response_data = {
                    'status': 'false',
                    'data': {},
                    'message': str(e),
                }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class RetrievePricing(APIView):
    def get(self,request,eventpricing_id):
        try:
            product = Pricing.objects.get(eventpricing_id=eventpricing_id)
            response_data = {
                    'status': 'true',
                    'data': {
                        'product_id': product.product_id,
                        'product_name': product.name,
                        'product_description': product.description,
                        'price_id': product.price_id,
                        'eventpricing_id': eventpricing_id,
                        'unit_amount': product.unit_amount,
                        'currency': product.currency,
                    },
                    'message': 'Product retrieved successfully',
                }
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            response_data = {
                    'status': 'false',
                    'data': {},
                    'message': str(e),
                }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        

class PricingList(APIView):
    
    def get(self, request): 
        try:
            queryset =  Pricing.objects.all().order_by('id')
            serializer = pricingSerializers(queryset, many=True)
            response_data = {
                'status': 'true',
                'data': serializer.data,
                'message': 'Products list retrieved successfully',
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Pricing.DoesNotExist:
            response_data = {
                'status': 'false',
                'data': {},
                'message': 'Product not found',
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        

            

class CreatePrice(APIView):

    def post(self, request):
        try:
            eventpricing_id = request.data.get('eventpricing_id')
            unit_amount = int(request.data.get('unit_amount'))
            currency = request.data.get('currency')
            amount_in_inr = unit_amount*100
            price = stripe.Price.create(
                product=eventpricing_id,
                unit_amount=amount_in_inr,
                currency=currency,

            )
            response_data = {
                    'status': 'true',
                    'data': {
                        'price_id': price.id,
                        'product_id': eventpricing_id, #prod_OLUy7TvVnQmrmC
                        'unit_amount': unit_amount,
                        'currency': currency,
                    },
                    'message': 'Price created successfully',
                }
            pricing = Pricing.objects.get(eventpricing_id=eventpricing_id)
            pricing.price_id = price.id
            pricing.unit_amount = unit_amount
            pricing.currency = currency
            pricing.save()
            return Response(response_data, status=status.HTTP_200_OK)       
        except Exception as e:
            response_data = {
                    'status': 'false',
                    'data': {},
                    'message': str(e),
                }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
      

''' api to connect to stripe for payment'''
#class PaymentView(LoginRequiredMixin, APIView):
class PaymentView(APIView):
    def get(self, request):

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
                print("event:",event_name)
                seats_booked = data.get('seats_booked','')
                event_start_time = data.get('event_start_time'),
                event_end_time = data.get('event_end_time')
                quantity = len(seats_booked)
                pricing = data.get('pricing','')
                pricing_dict = pricing[0]
                pricing_table_id = pricing_dict.get('id','')
                print(pricing_table_id)
                if pricing_table_id:
                    pricing_query = Pricing.objects.get(id=pricing_table_id)
                    print(pricing_query,"--------------------------------")
                    pricing_id = pricing_query.price_id
                    unit_amount = pricing_query.unit_amount
                    total_amount = unit_amount*quantity
                    print("Pricing ID:", pricing_id)
                    print("Unit Amount:", unit_amount)

                    line_items = [{'price':pricing_id,'quantity':quantity}]
  
                    session = stripe.checkout.Session.create(
                        payment_method_types=['card'],
                        line_items=line_items,
                        mode='payment',
                        success_url=request.build_absolute_uri('/payment_success_page/'),
                        cancel_url=request.build_absolute_uri('/payment_cancel_page/'),
                    )
                    print(session)
                    payment_status = session.status
                    print(payment_status)
                    session_id=session.id
                    data = {
                            'event_name':event_name,
                            'seats_booked':seats_booked,
                            'unit_amount':unit_amount,
                            'total_amount':total_amount,
                            'event_start_time':event_start_time,
                            'event_end_time':event_end_time,
                            'session_id':session_id,
                            }
                    event_query = Event.objects.get(event_name=event_name)
                    payment = Payment.objects.create(
                        user=user,
                        event=event_query,
                        session_id=session.id,
                        amount=unit_amount * quantity,
                        event_booking=booking,
                        )
               
                    response_data = {
                        'status': 'success',
                        'message': 'Redirecting to payment page',
                        'redirect_url': session.url,
                        'data': data
                    }
                    return Response(response_data, status=status.HTTP_200_OK)          

        response_data = {
                        'status': 'fail',
                        'message': 'Payment request failed!',
                        'redirect_url': '',
                        'data': data
                    }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class PaymentSuccess(APIView):

    def get(self, request):
        user_id = request.query_params.get('user_id')
        booking_id = request.query_params.get('booking_id')

        try:
            booking = EventBookings.objects.filter(id=booking_id, user_id=user_id)
            if booking.exists():
                latest_booking = booking.last()
                print(latest_booking)

                payment = Payment.objects.filter(event=latest_booking.event, user=latest_booking.user, status=0).first()
                if not payment:
                    response_data = {
                        'status': False,
                        'message': 'No pending payments!',
                    }
                    return Response(response_data, status=status.HTTP_200_OK)

                else:
                    payment.status = 1
                    payment.save()

                booking_serializer = eventbookingdisplaySerializers(latest_booking)
                booking_data = booking_serializer.data
                print("booking data: ", booking_data)
                serializer = paymentSerializers(payment)
                data = serializer.data
                print("data---------------",data)
                transaction_id = data.get('session_id','N/A')
                total_amount = data.get('amount','N/A')
                seats_booked = booking_data.get('seats_booked','')
                print(seats_booked)
                event_name = booking_data.get('event_name','N/A')
                event_start_time = booking_data.get('event_start_time','N/A')
                event_end_time = booking_data.get('event_end_time','N/A')
                ticket_info = {
                    "user":user_id,
                    "booking_id":booking_id,
                    "transaction_id":transaction_id,
                    "event_name":event_name,
                    "seats_booked":seats_booked,
                    "event_start_time":event_start_time,
                    "event_end_time":event_end_time,
                    "total_amount":total_amount,
                }
                self.createticketcollection(ticket_info)
                print("ticket data for event",ticket_info)

                user = User.objects.get(id=user_id)
                emailid=user.email
                first_name = user.first_name
                last_name = user.last_name
                user_name = first_name + " " + last_name
                ticket_info["user_name"] = user_name
                total_booked_seats = len(seats_booked)
                ticket_info["total_booked_seats"] = total_booked_seats
                new_seats_booked = ', '.join(str(item) for item in seats_booked)
                if "seats_booked" in ticket_info:
                    ticket_info["seats_booked"] = new_seats_booked
                self.sent_ticket_mail(ticket_info, emailid)
                # try:
                #     ticket_info['_id'] = str(ticket_info['_id'])
                #     ticket_collection.insert_one(ticket_info)
                response_data = {
                        'status': True,
                        #'ticket_info': ticket_info,
                        'message': 'Payment status updated and ticket generated!',
                    }
                return Response(response_data, status=status.HTTP_201_CREATED)

            else:
                return Response({'status': False, 'message': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)


        except Payment.DoesNotExist:
            response_data = {
                        'status': False,
                        'message': 'No Booking found with this id!',
                    }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
    def createticketcollection(self, records):
        records = records
     
        ticket_collection.insert_one(records)
        print("inserted record")
        return True
    
    def sent_ticket_mail(self,context, emailid):
   
        to = [emailid] 
        htmly = get_template('email_ticket_template.html')
        subject = "Ticket"
        text_content = ""
        html_content = htmly.render(context)
        self.sent_mail_with_template(subject, html_content, text_content, to)
        pass

    def sent_mail_with_template(self,subject, html_content, text_content, to):
        pdf_ticket = pdfkit.from_string(html_content, False)
        msg = EmailMultiAlternatives(subject, text_content, to=to)
        msg.attach_alternative(html_content, "text/html")
        msg.attach("ticket.pdf", pdf_ticket, "application/pdf")
        msg.send()
        print(" email send success")


class RetrieveTicket(APIView):
    def get(self, request):
    
        user_id = request.query_params.get('user_id')
        booking_id = request.query_params.get('booking_id')

        if not user_id or not booking_id:
            payload = {
                "status": False,
                "message": "Both user_id and booking_id are required.",
                }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        query = {
            "user": user_id,
            "booking_id": booking_id,
        }
        response_data={}
        try:
            matching_documents = ticket_collection.find(query)
            for document in matching_documents:
                document = document
                print(document)
                print(type(document))
                transaction_id = document.get('transaction_id','N/A')
                user_id = document.get('user')

                user = User.objects.get(id=user_id)
                first_name = user.first_name
                last_name = user.last_name
                user_name = first_name + " " + last_name
                event_name = document.get('event_name','N/A')
                seats_booked = document.get('seats_booked','N/A')
                event_start_time = document.get('event_start_time','N/A')
                event_end_time = document.get('event_end_time','N/A')
                total_amount = document.get('total_amount','N/A')
                total_booked_seats = len(seats_booked)
                ticket_dict = {
                    'transaction_id': transaction_id,
                    'user_name': user_name,
                    'event_name': event_name,
                    'seats_booked': seats_booked,
                    'event_start_time': event_start_time,
                    'event_end_time': event_end_time,
                    'total_amount': total_amount,
                    'total_booked_seats': total_booked_seats,
                }
                response_data = {
                    'status': True,
                    'data': ticket_dict,
                    'message': 'Data retrieved Successfully!',
                }
            
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({
                'status': False, 
                'message': 'Failed'}, status=status.HTTP_404_NOT_FOUND)



def generate_pdf(request):

    user_id = request.GET.get('user_id')
    booking_id = request.GET.get('booking_id')
    if not user_id or not booking_id:
        payload = {
                "status": False,
                "message": "Both user_id and booking_id are required.",
                }
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    query = {
        "user": user_id,
        "booking_id": booking_id,
    }

    matching_documents = ticket_collection.find(query)
    for document in matching_documents:
        print(document,"===================document_type========================")
        document = document
        transaction_id = document.get('transaction_id','N/A')
        user_id = document.get('user')

        user = User.objects.get(id=user_id)
        first_name = user.first_name
        last_name = user.last_name
        user_name = first_name + " " + last_name
        event_name = document.get('event_name','N/A')
        seat_booked = document.get('seats_booked','N/A')
        total_booked_seats = len(seat_booked)
        seats_booked = ', '.join(str(item) for item in seat_booked)
        event_start_time = document.get('event_start_time','N/A')
        event_end_time = document.get('event_end_time','N/A')
        total_amount = document.get('total_amount','N/A')
     
        context = {
            'transaction_id': transaction_id,
            'user_name': user_name,
            'event_name': event_name,
            'seats_booked': seats_booked,
            'event_start_time': event_start_time,
            'event_end_time': event_end_time,
            'total_amount': total_amount,
            'total_booked_seats': total_booked_seats,
        }

    template = get_template('ticket_template.html')
    html_content = template.render(context)

    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
    }
    pdf = pdfkit.from_string(html_content, False, options=options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="ticket.pdf"'
    return response


'''retrieve all payments of user based on user id'''

class RetrievePayments(APIView):

    def get(self, request):

        user_id = request.GET.get('user_id')
        if not user_id:
            payload = {
                    "status": False,
                    "message": "user_id is required.",
                    }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        else:
            payments = Payment.objects.filter(user=user_id).order_by('-id')
            print("Payments:",payments)

            serializers = paymentSerializers(payments,many=True)
            data = serializers.data

            event_ids = set(item['event'] for item in data)
            event_booking_ids = set(item['event_booking'] for item in data if item['event_booking'] is not None)
            events_info = {}
            booking_info = {}
            for event_id in event_ids:
                try:
                    event = Event.objects.get(pk=event_id)
                    event_start_time = str(event.event_start_time)
                    event_start_time = self.convert_datetime_format(event_start_time)
                    event_end_time = str(event.event_end_time)
                    event_end_time = self.convert_datetime_format(event_end_time)
                    event_info = {
                        'event_id': event.id,
                        'event_name': event.event_name,
                        'event_start_time': event_start_time,
                        'event_end_time': event_end_time,
                    }
                    events_info[event_id] = event_info
                except Event.DoesNotExist:
                    pass
            for event_booking in event_booking_ids:
                try:
                    eventbooking = EventBookings.objects.get(id=event_booking)
                    seats_booked = eventbooking.seats_booked
                    total_booked_seats = len(seats_booked)
                    seats_booked = ', '.join(str(item) for item in seats_booked)
                    booking_info[event_booking] = {
                        'event_booking': event_booking,
                        'seats_booked': seats_booked,
                        'total_booked_seats' : total_booked_seats
                    }
                except Event.DoesNotExist:
                    pass

        
            for item in data:
                item["status"] = self.update_status(item["status"])
                event_id = item['event']
                if event_id in events_info:
                    item.update(events_info[event_id])
                if event_booking in booking_info:
                    item.update(booking_info[event_booking])
            response_data = {
                'data': data,
                'status': 'success',
                'message':"Data retrieved successfully"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
    def convert_datetime_format(self,input_datetime):

        dt = datetime.fromisoformat(input_datetime.replace('Z', '+00:00'))
        formatted_datetime = dt.strftime('%b %d, %Y %I:%M %p')   
        return formatted_datetime
    
    def update_status(self,status):

        if status == 0 or status == 2:
            return "Pending"
        elif status == 1:
            return "Paid"


class SentTicketMail(APIView):
   
    def get(self,request):
        # to = [user_email]
        htmly = get_template('email_ticket_template.html')
        subject = "Ticket"
        text_content = ""
        html_content = htmly.render({
                "transaction_id": "cs_test_a1wSYDx37oULe4xTJeRNZkgNKXj3YtynMjrhOYJQOmBiapy8ornFOorWW7",
                "user_name": "test testtester",
                "event_name": "event two",
                "seats_booked": [64],
                "event_start_time": "Jul 09, 2023 06:18 AM",
                "event_end_time": "Jul 27, 2023 06:00 PM",
                "total_amount": "500.00",
                "total_booked_seats": 1,
            })
        self.sent_mail_with_template(subject, html_content, text_content, to)
        pass

    def sent_mail_with_template(self,subject, html_content, text_content, to):
        pdf_ticket = pdfkit.from_string(html_content, False)

        # Create email message and attach the PDF ticket
        msg = EmailMultiAlternatives(subject, text_content, to=to)
        msg.attach_alternative(html_content, "text/html")
        msg.attach("ticket.pdf", pdf_ticket, "application/pdf")
        msg.send()
        print(" email send success")
        



''' TEMPLATE URLS  '''

def eventpage(request):
    return render(request, 'userevent.html')

def adminlogin(request):
    return render(request, 'admin_login.html')

def adminsignup(request):
    return render(request, 'admin_signup.html')

def ticket(request):
    return render(request, 'ticket.html')

def pricingpage(request):
    return render(request, 'price_list.html')

def paymentpage(request):
    return render(request, 'payment_home.html')

def paymentlistingpage(request):
    return render(request, 'payment_listpage.html')


class TicketCollectionAPIView(APIView):
    def get(self, request):
        ticket_collections = TicketCollection.objects.all()
        serializer = TicketCollectionSerializer(ticket_collections, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TicketCollectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)