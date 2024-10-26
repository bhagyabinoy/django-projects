from django.contrib import admin
from django.urls import path
from .views import *



urlpatterns = [
path('createpricing/', CreatePricing.as_view(), name='create_pricing'),
path('retrievepricing/<str:product_id>/', RetrievePricing.as_view(), name='retrieve_pricing'),
path('createprice/', CreatePrice.as_view(), name='retrieve_product'),
path('productlist/', PricingList.as_view(), name='retrieve_stripeproduct_list'),
path('paymentview/', PaymentView.as_view(), name='choose_plan'),
path('payment_success/', PaymentSuccess.as_view(), name='payment_success_and_generate_ticket'),
path('retrieve/', RetrieveTicket.as_view(), name='retrieve_ticket'), 
path('ticketcollection/', TicketCollectionAPIView.as_view(), name='ticketcollection'),
path('generate-pdf/', generate_pdf, name='generate_pdf'),
path('retrievepayments/', RetrievePayments.as_view(), name='retrieve_payments'), 
path('email/',SentTicketMail.as_view(), name='sent_ticket_mail'),



#template 
path('event/',eventpage, name='eventpage'),
path('adminlogin/',adminlogin, name='adminlogin'),
path('adminsignup/',adminsignup, name='adminsignup'),
path('',ticket, name='ticket'),
path('paymentpage/',paymentpage, name='paymentpage'),
path('paymentlistingpage/',paymentlistingpage, name='paymentlistingpage'), 
path('pricingpage/',pricingpage, name='pricingpage'),
]

#http://127.0.0.1:8000/ticket/generate-pdf/?user_id=1&booking_id=33