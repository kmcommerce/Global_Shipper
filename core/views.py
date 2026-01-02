
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect

def index(request):
    return render(request, "core/index.html")

def faq_view(request):
    faqs = [
        {
            'question': 'How do I create an order?',
            'answer': 'Login to your account, select a service, fill in shipment details, and checkout.'
        },
        {
            'question': 'What payment methods do you accept?',
            'answer': 'We accept Credit/Debit Card, Bank Transfer, Wire, CashApp, Zelle, Apple Pay, and Cash.'
        },
        {
            'question': 'How can I track my order?',
            'answer': 'Go to your account dashboard and click on "Track Orders".'
        },
        {
            'question': 'Do you ship internationally?',
            'answer': 'Yes! Currently we ship from North America, China, and Europe to West & Central Africa.'
        },
    ]
    return render(request, 'core/faq.html', {'faqs': faqs})

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        full_message = f"Message from {name} ({email}):\n\n{message}"

        send_mail(
            subject=f"Contact Form Submission from {name}",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False
        )

        messages.success(request, "Thank you! Your message has been sent.")
        return redirect('core:contact')

    return render(request, 'core/contact.html')



