
from decimal import Decimal
from django.core.mail import send_mail
from django.conf import settings
from .utils import send_order_status_email



PICKUP_FEE = Decimal('50.00')


def calculate_price(service, weight_kg, volume_cbm, pickup_required):
    base_price = service.base_price

    if service.service_type == 'DTD':
        cost = base_price + (Decimal(weight_kg) * Decimal('2.0'))

    elif service.service_type == 'LCL':
        cost = base_price + (Decimal(volume_cbm) * Decimal('75.0'))

    elif service.service_type == 'FCL':
        cost = base_price  # flat rate

    else:
        cost = base_price

    pickup_fee = PICKUP_FEE if pickup_required else Decimal('0.00')

    total = cost + pickup_fee

    return cost, pickup_fee, total


def send_order_confirmation_email(order):
    subject = f'GlobalShipper Order Confirmation - #{order.id}'
    
    html_message = f"""
<html>
<body>
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; border:1px solid #ddd; padding:20px;">
        <div style="text-align:center;">
            <img src="https://yourdomain.com/static/images/logo.png" alt="GlobalShipper Logo" width="200"/>
            <h2>Thank you for your order!</h2>
        </div>
        <p>Hello {order.user.get_full_name() or order.user.username},</p>
        <p>Your order has been received. Here are the details:</p>
        <ul>
            <li>Service: {order.service.name}</li>
            <li>Origin: {order.origin_country}</li>
            <li>Destination: {order.destination_country}</li>
            <li>Weight: {order.weight_kg} kg</li>
            <li>Volume: {order.volume_cbm} CBM</li>
            <li>Tax: ${order.tax_amount}</li>
            <li>Total Amount: ${order.total_amount}</li>
            <li>Payment Method: {order.get_payment_method_display()}</li>
            <li>Status: {order.payment_status}</li>
        </ul>
        <p>We will notify you when the status changes.</p>
        <p>Thank you for choosing <strong>GlobalShipper</strong>!</p>
    </div>
</body>
</html>
"""
    send_mail(
        subject,
        '',
        settings.DEFAULT_FROM_EMAIL,
        [order.user.email],
        html_message=html_message,
        fail_silently=True
    )



def send_order_status_email(order):
    """
    Send email to customer when order status changes.
    """
    subject = f'GlobalShipper Order Update - #{order.id}'
    message = f"""
Hello {order.user.get_full_name() or order.user.username},

Your order #{order.id} has been updated.

Current Status: {order.get_status_display()}
Payment Status: {order.get_payment_status_display()}

Service: {order.service.name}
Origin: {order.origin_country}
Destination: {order.destination_country}
Total Amount: ${order.total_amount}

Thank you for using GlobalShipper!
"""
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.user.email], fail_silently=True)

@admin.action(description='Mark selected orders as Paid')
def mark_as_paid(modeladmin, request, queryset):
    updated_count = queryset.update(status='paid', payment_status='paid')
    for order in queryset:
        send_order_status_email(order)
    modeladmin.message_user(
        request,
        f"{updated_count} order(s) marked as Paid and customers notified."
    )