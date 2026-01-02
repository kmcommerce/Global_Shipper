
import random
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta


VERIFICATION_EXPIRY_MINUTES = 10


def generate_verification_code():
    return str(random.randint(100000, 999999))


def is_code_expired(created_at):
    if not created_at:
        return True
    return timezone.now() > created_at + timedelta(minutes=VERIFICATION_EXPIRY_MINUTES)


def send_email_verification(user):
    code = generate_verification_code()

    user.email_verification_code = code
    user.verification_code_created_at = timezone.now()
    user.save(update_fields=[
        "email_verification_code",
        "verification_code_created_at"
    ])

    send_mail(
        subject="GlobalShipper - Email Verification Code",
        message=f"Your verification code is: {code}\n\nThis code expires in 10 minutes.",
        from_email="noreply@globalshipper.com",
        recipient_list=[user.email],
        fail_silently=False,
    )


def send_phone_verification(user):
    code = generate_verification_code()

    user.phone_verification_code = code
    user.verification_code_created_at = timezone.now()
    user.save(update_fields=[
        "phone_verification_code",
        "verification_code_created_at"
    ])

    # MVP placeholder
    print(f"[SMS] Send {code} to {user.phone_number}")
