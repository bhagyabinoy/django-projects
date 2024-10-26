from django.urls import path
from .views import *
urlpatterns = [
        path('paymenthome/',paymenthome, name='paymenthome'),
        path('createproduct/', CreateProduct.as_view(), name='create_product'),
        path('retrieveproduct/<str:product_id>/', RetrieveProduct.as_view(), name='retrieve_product'),
        path('createprice/', CreatePrice.as_view(), name='retrieve_product'),
        path('productlist/', ProductList.as_view(), name='retrieve_product_list'),
        path('paymentview/', PaymentView.as_view(), name='choose_plan'),
        path('payment_success/', PaymentSuccess.as_view(), name='payment_success'),
        path('retrievecart/', CartView.as_view(), name='retrieve'),
        path('payment_cancel/', payment_cancel_page, name='payment_cancel_page'),
        path('payment_success_page/', payment_success_page, name='payment_success'),
        path('product_page/', productpage, name='payment_success'),
        path('webhook/', stripe_webhook, name='stripe_webhook'),
        
        path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
        path('cart/remove/', RemoveFromCartView.as_view(), name='remove_from_cart'),
        path('cart/update/', UpdateCartView.as_view(), name='update_cart'),
        path('cart/count/', CartCountView.as_view(), name='cart_count'),
        path('cart/products/', ProductsInCartView.as_view(), name='cart_product_view'),
        path('cart/view/', cartpage, name='cart_page'),
 

]