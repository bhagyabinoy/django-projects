import stripe
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User



# Set up Stripe API keys
stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentView(LoginRequiredMixin, APIView):
    def get(self, request):
        print("called Payment View")
        print(request.data)
        plan = request.POST.get('plan', '')
        print(plan)
        if plan == 'monthly':
            price_id = 'price_1NDKnOSGBtI1Sz1AyKbshYYS'
            print(price_id)
        elif plan == 'yearly':
            price_id = 'price_1NDKp7SGBtI1Sz1AolqbNL1A'
        else:
            response_data = {
                'status': 'error',
                'message': 'Invalid request',
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=request.build_absolute_uri('/payment_success_page/'),
            cancel_url=request.build_absolute_uri('/payment_cancel_page/'),
        )
        print("url to redirect :",session.url)
        subscription_id = session.subscription
        #subscription = stripe.Subscription.retrieve(subscription_id)
        # created_date = subscription.created
        # end_date = subscription.current_period_end
        # print(created_date)
        # print(end_date)
        print(subscription_id)
        response_data = {
                'status': 'success',
                'message': 'redirecting to payment page',
                'redirect_url':session.url,
            }
        return Response(response_data, status=status.HTTP_200_OK)


class PaymentSuccess(LoginRequiredMixin, APIView):

    def get(self, request):
        user_email = request.query_params.get('user')  
        plan = request.query_params.get('plan')  
        user = User.objects.get(email=user_email)
        print(user)
        user.premium_member = True
        user.plan = plan
        user.save()
        response_data = {
            'status': 'success',
            'message': 'Payment successful!',
        }
        return Response(response_data, status=status.HTTP_200_OK)

def choose_plan_page(request):
    return render(request, 'choose_plan.html') 

def payment_cancel_page(request):
    return render(request, 'payment_cancel.html') 

def payment_success_page(request):
    return render(request, 'payment_success.html')  
