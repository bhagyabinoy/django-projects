from django.shortcuts import render
import stripe
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from .serializers import *
from .models  import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateProduct(APIView):

    def post(self,request):
        try:
            name = request.data.get('name')
            product_type = request.data.get('product_type')
            description = request.data.get('description')

            product = stripe.Product.create(
                name=name,
                type=product_type,
                description=description
            )
            product_obj = Product.objects.create(
                product_id=product.id,
                name=product.name,
                description=product.description
            )
            print(product_obj)
            response_data = {
                    'status': 'true',
                    'data': {
                        'product_id': product.id,
                        'product_name': product.name,
                        'product_description': product.description,
                    },
                    'message': 'Product created successfully',
                }
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            response_data = {
                    'status': 'false',
                    'data': {},
                    'message': str(e),
                }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class RetrieveProduct(APIView):
    def get(self,request,product_id):
        try:
            product = Product.objects.get(product_id=product_id)
            response_data = {
                    'status': 'true',
                    'data': {
                        'product_id': product.product_id,
                        'product_name': product.name,
                        'product_description': product.description,
                        'price_id': product.price_id,
                        'product_id': product_id,
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
        

class ProductList(APIView):
    
    def get(self, request): 
        try:
            queryset =  Product.objects.all().order_by('id')
            serializer = ProductSerializer(queryset, many=True)
            response_data = {
                'status': 'true',
                'data': serializer.data,
                'message': 'Products list retrieved successfully',
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Product.DoesNotExist:
            response_data = {
                'status': 'false',
                'data': {},
                'message': 'Product not found',
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            

class CreatePrice(APIView):

    def post(self, request):
        try:
            product_id = request.data.get('product_id')
            unit_amount = int(request.data.get('unit_amount'))
            currency = request.data.get('currency')
            amount_in_inr = unit_amount*100
            price = stripe.Price.create(
                product=product_id,
                unit_amount=amount_in_inr,
                currency=currency,

            )
            response_data = {
                    'status': 'true',
                    'data': {
                        'price_id': price.id,
                        'product_id': product_id,
                        'unit_amount': unit_amount,
                        'currency': currency,
                    },
                    'message': 'Price created successfully',
                }
            product = Product.objects.get(product_id=product_id)
            product.price_id = price.id
            product.unit_amount = unit_amount
            product.currency = currency
            product.save()
            return Response(response_data, status=status.HTTP_200_OK)       
        except Exception as e:
            response_data = {
                    'status': 'false',
                    'data': {},
                    'message': str(e),
                }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
      

class PaymentView(LoginRequiredMixin, APIView):
    def get(self, request):
        try:
            user_email = request.query_params.get('user')
            print(user_email)
            
            try:
                user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                response_data = {
                    'status': 'false',
                    'message': 'User does not exist',
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            
            cart_items = CartItem.objects.filter(user=user)
            line_items = []
            
            for cart_item in cart_items:
                product = cart_item.product      
                print(product)
                print(product.price_id)
                print("price,",product.unit_amount)
                line_items.append({
                    'price': product.price_id, 
                    'quantity': cart_item.quantity,
                })

            
        except Exception as e:
            response_data = {
                'status': 'false',
                'message': str(e),
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri('/payment_success_page/'),
            cancel_url=request.build_absolute_uri('/payment_cancel_page/'),
        )
        print(session)
        for cart_item in cart_items:
            product = cart_item.product
            payment = Payment.objects.create(
                user=user,
                product=product,
                session_id=session.id,
                amount=product.unit_amount * cart_item.quantity,
            )

        #creating order object
        order=Orders.objects.create(user=user,session_id=session.id)
        payments = Payment.objects.filter(user=user, session_id=session.id)
        for payment in payments:
            print(payment.product)
            print(payment.amount)
        print(payments)
        response_data = {
            'status': 'success',
            'message': 'Redirecting to payment page',
            'redirect_url': session.url,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class PaymentSuccess(LoginRequiredMixin, APIView):

    def get(self, request):
        user_email = request.query_params.get('user')  
        user = User.objects.get(email=user_email)
        print(user,"------------user------------")
        cart_items = CartItem.objects.filter(user=user)
        cart_items.delete()
        response_data = {
            'status': 'success',
            'message': 'Payment successful!',
        }
        return Response(response_data, status=status.HTTP_200_OK)


# class SubscriptionPaymentSuccess(LoginRequiredMixin, APIView):

#     def get(self, request):
#         user_email = request.query_params.get('user')  
#         plan = request.query_params.get('plan')  
#         user = User.objects.get(email=user_email)
#         print(user)
#         user.premium_member = True
#         user.plan = plan
#         user.save()
#         response_data = {
#             'status': 'success',
#             'message': 'Payment successful!',
#         }
#         return Response(response_data, status=status.HTTP_200_OK)


class CartView(APIView):
    
    def get(self, request): 
            queryset =  CartItem.objects.all().order_by('id')
            serializer = CartItemSerializer(queryset, many=True)
            response_data = {
                'status': 'true',
                'data': serializer.data,
                'message': 'CartItem retrieved successfully',
            }
            return Response(response_data, status=status.HTTP_200_OK)
    

class AddToCartView(APIView):
    def post(self, request):
        user_email = request.POST.get('user')
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        print(product_id)
        try:
            try:
                user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                response_data = {
                    'status': 'false',
                    'message': 'User does not exist',
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            try:
                cart_item = CartItem.objects.get(user=user, product__product_id=product_id)
                cart_item.quantity += quantity
                cart_item.save()
            except CartItem.DoesNotExist:
                product = Product.objects.get(product_id=product_id)
                cart_item = CartItem.objects.create(user=user, product=product, quantity=quantity)
            
            response_data = {
                'status': 'true',
                'message': 'Product added to cart successfully',
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            response_data = {
                'status': 'false',
                'message': str(e),
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class ProductsInCartView(LoginRequiredMixin, APIView):
    def get(self, request):
        try:
            user_email = request.query_params.get('user')
            print(user_email)
            
            try:
                user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                response_data = {
                    'status': 'false',
                    'message': 'User does not exist',
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            
            cart_items = CartItem.objects.filter(user=user)
            data = []
            
            for cart_item in cart_items:
                product = cart_item.product      
                print(product)
                data.append({
                    'product_id': product.product_id,
                    'name': product.name,
                    'description': product.description,
                    'price_id': product.price_id,
                    'unit_amount': str(product.unit_amount),
                    'currency': product.currency,
                    'quantity': cart_item.quantity,
                })
            
            response_data = {
                'status': 'true',
                'data': data,
                'message': 'Products in cart retrieved successfully',
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            response_data = {
                'status': 'false',
                'message': str(e),
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
class CartCountView(LoginRequiredMixin, APIView):
    def get(self, request):
        user_email = request.query_params.get('user')
        try:
            try:
                user = User.objects.get(email=user_email)
                count = CartItem.objects.filter(user=user).count()
                response_data = {
                    'status': 'true',
                    'count': count
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                response_data = {
                    'status': 'false',
                    'message': 'User does not exist',
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response_data = {
                'status': 'false',
                'message': str(e),
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class UpdateCartView(LoginRequiredMixin, APIView):
    def post(self, request):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        user_email = request.POST.get('user')
        try:
            try:
                user = User.objects.get(email=user_email) 
            except User.DoesNotExist:
                response_data = {
                    'status': 'false',
                    'message': 'User does not exist',
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            
            product = Product.objects.get(product_id=product_id)
            cart_item, created = CartItem.objects.get_or_create(user=user, product=product)
            cart_item.quantity = quantity
            cart_item.save()
            
            response_data = {
                'status': 'true',
                'message': 'Cart updated successfully',
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            response_data = {
                'status': 'false',
                'message': 'Product does not exist',
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response_data = {
                'status': 'false',
                'message': str(e),
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class RemoveFromCartView(LoginRequiredMixin, APIView):
    def get(self, request):
        product_id = request.query_params.get('product_id')
        print(product_id)
        user_email = request.query_params.get('user')
        print(user_email)
        try:
            try:
                user = User.objects.get(email=user_email) 
            except User.DoesNotExist:
                response_data = {
                    'status': 'false',
                    'message': 'User does not exist',
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            product = Product.objects.get(product_id=product_id)
            cart_item = CartItem.objects.get(user=user, product=product)
            cart_item.delete()
            response_data = {
                'status': 'true',
                'message': 'Product removed from cart successfully'
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            response_data = {
                'status': 'false',
                'message': 'CartItem does not exist',
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            response_data = {
                'status': 'false',
                'message': 'Product does not exist',
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response_data = {
                'status': 'false',
                'message': str(e),
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    print("----payload-----",payload)
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        print(e)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        print(payment_intent)

    elif event.type == 'charge.failed':
        charge = event.data.object
        print(charge)
    return JsonResponse({'status': 'success'})


        
#templates
def payment_cancel_page(request):
    return render(request, 'payment_cancel.html') 

def payment_success_page(request):
    return render(request, 'payment_success.html')  

def paymenthome(request):
    return render(request, 'payment_home.html')

def productpage(request):
    return render(request, 'product.html')

def cartpage(request):
    return render(request, 'cart_page.html')




