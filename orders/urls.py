from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Order Listing & Success
    path('my/', views.my_orders_view, name='my_orders'),
    path('fcl/quote/submitted/', views.quote_submitted_view, name='quote_submitted'),
    
    # Quote & Order Detail (using UUID)
    path('<uuid:order_id>/', views.order_detail_view, name='order_detail'),
    path('quote/<uuid:order_id>/accept/', views.accept_quote_view, name='accept_quote'),
    
    # Form/Quote Creation
    path('fcl/quote/', views.fcl_quote_view, name='fcl_quote'),
    
    # Payments (Stripe & Instructions)
    path('pay/<uuid:order_id>/', views.stripe_checkout_view, name='stripe_checkout'),
    path('payment-success/<uuid:order_id>/', views.payment_success_view, name='payment_success'),
    path('<uuid:order_id>/payment/', views.payment_selection_view, name='payment_select'),
    path('<uuid:order_id>/instructions/', views.payment_instructions_view, name='payment_instructions'),
]