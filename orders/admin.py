from django.contrib import admin
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum
from django.utils.html import format_html

from .models import Order


# -------------------------------------------------
# Admin Dashboard Summary (Top of Admin)
# -------------------------------------------------
def payment_summary(modeladmin, request):
    paid_total = (
        Order.objects
        .filter(payment_status="paid")
        .aggregate(total=Sum("quoted_total"))["total"] or 0
    )

    pending_count = Order.objects.filter(payment_status="pending").count()
    quote_count = Order.objects.filter(quote_status="new").count()

    return format_html(
        """
        <div style="padding:15px">
            <h2>📊 Payment Summary</h2>
            <p><strong>Total Paid:</strong> ${}</p>
            <p><strong>Pending Payments:</strong> {}</p>
            <p><strong>New Quote Requests:</strong> {}</p>
        </div>
        """,
        paid_total,
        pending_count,
        quote_count,
    )


# -------------------------------------------------
# Admin Actions
# -------------------------------------------------
@admin.action(description="Send quote email to customer")
def send_quote_email(modeladmin, request, queryset):
    sent_count = 0

    for order in queryset:
        if order.quoted_total and order.quote_status == "new":
            send_mail(
                subject="Your Shipping Quote – Ship 2 Africa",
                message=f"""
Hello {order.customer.first_name or 'Customer'},

Thank you for requesting a shipping quote with Ship 2 Africa.

Service Type: {order.get_service_type_display()}
Destination: {order.destination_country}

Ocean Freight (Maersk): ${order.maersk_ocean_rate}
Booking Fee: ${order.booking_fee}

----------------------------------
TOTAL QUOTE: ${order.quoted_total}
----------------------------------

To accept this quote, please log in to your account.

Thank you,
Ship 2 Africa Team
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.customer.email],
                fail_silently=True,
            )

            order.quote_status = "quoted"
            order.quote_sent_at = timezone.now()
            order.save()

            sent_count += 1

    modeladmin.message_user(
        request,
        f"{sent_count} quote email(s) sent successfully."
    )


@admin.action(description="Mark selected orders as paid & notify customer")
def mark_as_paid(modeladmin, request, queryset):
    for order in queryset:
        order.payment_status = "paid"
        order.save()

        send_mail(
            subject="Payment Confirmed – Ship 2 Africa",
            message=f"""
Hello {order.customer.get_full_name() or order.customer.username},

We have received your payment for Order #{order.id}.

Service: {order.get_service_type_display()}
Amount Paid: ${order.quoted_total}

Your shipment is now being processed.

Thank you,
Ship 2 Africa Team
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.customer.email],
            fail_silently=True,
        )


# -------------------------------------------------
# Order Admin Configuration
# -------------------------------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "service_type",
        "destination_country",
        "quote_status",
        "payment_status",
        "quoted_total",
        "created_at",
    )

    list_filter = (
        "service_type",
        "quote_status",
        "payment_status",
    )

    search_fields = (
        "id",
        "customer__email",
    )

    actions = [
        send_quote_email,
        mark_as_paid,
    ]


# Branding
admin.site.site_header = "Ship 2 Africa Admin"
admin.site.site_title = "Ship 2 Africa"
admin.site.index_title = "Operations Dashboard"
