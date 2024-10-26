from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
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
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives



class GenerateEmail:

    def __init__(self):
        pass

    def generate_pdf(user_id,booking_id):

        query = {
            "user": user_id,
            "booking_id": booking_id,
        }

        matching_documents = ticket_collection.find(query)
        for document in matching_documents:
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
        #response['Content-Disposition'] = 'attachment; filename="ticket.pdf"'
        return response