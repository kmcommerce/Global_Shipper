
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .payment_instructions import PAYMENT_INSTRUCTIONS
from .models import Order
from .forms import FCLQuoteForm
import stripe

if settings.STRIPE_SECRET_KEY:
    stripe.api_key = settings.STRIPE_SECRET_KEY

# -----------------------------------
# FCL QUOTE REQUEST (Customer)
# -----------------------------------
@login_required
def fcl_quote_view(request):
    if request.method == "POST":
        form = FCLQuoteForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user
            order.service_type = "FCL"
            order.quote_status = "new"
            order.save()

            messages.success(
                request,
                "Your FCL quote request has been submitted. Our team will review it shortly."
            )
            return redirect("orders:quote_submitted")
    else:
        form = FCLQuoteForm()

    return render(request, "orders/fcl_quote.html", {"form": form})


# -----------------------------------
# QUOTE SUBMITTED CONFIRMATION
# -----------------------------------
@login_required
def quote_submitted_view(request):
    return render(request, "orders/quote_submitted.html")


# -----------------------------------
# CUSTOMER ORDER LIST
# -----------------------------------
@login_required
def my_orders_view(request):
    orders = Order.objects.filter(customer=request.user).order_by("-created_at")
    return render(request, "orders/my_orders.html", {"orders": orders})


# -----------------------------------
# ORDER DETAIL (Customer)
# -----------------------------------
@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, "orders/order_detail.html", {"order": order})


# -----------------------------------
# ACCEPT QUOTE (Customer)
# -----------------------------------
@login_required
def accept_quote_view(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user,
        quote_status="quoted",
    )

    if request.method == "POST":
        order.quote_status = "accepted"
        order.quote_accepted_at = timezone.now()
        order.save()

        messages.success(
            request,
            "Quote accepted. You may now proceed to payment."
        )

        return redirect("orders:order_detail", order_id=order.id)

@login_required
def stripe_checkout_view(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user,
        quote_status='accepted',
        payment_status='unpaid'
    )

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(order.quoted_total * 100),
                'product_data': {
                    'name': f'FCL Shipping – Order {order.id}',
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(
            f'/orders/payment-success/{order.id}/'
        ),
        cancel_url=request.build_absolute_uri(
            f'/orders/{order.id}/'
        ),
    )

    order.stripe_session_id = session.id
    order.save()

    return redirect(session.url)

@login_required
def payment_success_view(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user
    )

    order.payment_status = 'paid'
    order.save()

    return render(request, 'orders/payment_success.html', {
        'order': order
    })

@login_required
def payment_selection_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    if request.method == "POST":
        method = request.POST.get("payment_method")
        order.payment_method = method
        order.payment_status = "pending"
        order.save()

        if method == "stripe":
            return redirect("orders:stripe_checkout", order_id=order.id)

        return redirect("orders:payment_instructions", order_id=order.id)

    return render(request, "orders/payment_select.html", {"order": order})

@login_required
def payment_instructions_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    instructions = PAYMENT_INSTRUCTIONS.get(order.payment_method)

    return render(
        request,
        "orders/payment_instructions.html",
        {
            "order": order,
            "instructions": instructions,
        }
    )



