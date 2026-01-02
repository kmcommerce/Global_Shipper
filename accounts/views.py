
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import ProfileUpdateForm

from .forms import SignUpForm, LoginForm, VerificationForm
from .models import User
from .utils import (
    send_email_verification,
    send_phone_verification,
    is_code_expired
)


def signup_view(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('core:index')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Store pending verification
            request.session['pending_user_id'] = user.id
            request.session['verification_method'] = 'email'

            send_email_verification(user)

            messages.success(
                request,
                'Account created! Please verify your email.'
            )
            return redirect('accounts:verify')
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


def verify_view(request):
    """Verification code entry"""
    user_id = request.session.get('pending_user_id')
    if not user_id:
        messages.error(request, 'No pending verification found.')
        return redirect('accounts:signup')

    user = User.objects.filter(id=user_id).first()
    if not user:
        messages.error(request, 'User not found.')
        return redirect('accounts:signup')

    verification_method = request.session.get('verification_method', 'email')

    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['verification_code']

            if is_code_expired(user.verification_code_created_at):
                messages.error(
                    request,
                    'Verification code expired. Please request a new one.'
                )
                return redirect('accounts:resend')

            if verification_method == 'email' and code == user.email_verification_code:
                user.is_email_verified = True
            elif verification_method == 'phone' and code == user.phone_verification_code:
                user.is_phone_verified = True
            else:
                messages.error(request, 'Invalid verification code.')
                return redirect('accounts:verify')

            user.is_active = True
            user.email_verification_code = None
            user.phone_verification_code = None
            user.save()

            login(request, user)
            request.session.pop('pending_user_id', None)
            request.session.pop('verification_method', None)

            messages.success(request, 'Account verified successfully!')
            return redirect('core:index')
    else:
        form = VerificationForm()

    return render(request, 'accounts/verify.html', {
        'form': form,
        'verification_method': verification_method
    })


@require_POST
@login_required
def switch_verification(request):
    method = request.POST.get("method")

    if method not in ["email", "phone"]:
        messages.error(request, "Invalid verification method.")
        return redirect("accounts:verify")

    user = request.user

    # Store preferred verification method on user or session
    # Option 1 (simplest): session-based
    request.session["verification_method"] = method

    messages.success(
        request,
        f"Verification method switched to {method}."
    )

    return redirect("accounts:verify")


def resend_code_view(request):
    """Resend verification code"""
    user_id = request.session.get('pending_user_id')
    if not user_id:
        messages.error(request, 'No pending verification found.')
        return redirect('accounts:signup')

    user = User.objects.filter(id=user_id).first()
    if not user:
        messages.error(request, 'User not found.')
        return redirect('accounts:signup')

    method = request.session.get('verification_method', 'email')

    if method == 'email':
        send_email_verification(user)
        messages.success(request, 'New email verification code sent.')
    else:
        send_phone_verification(user)
        messages.success(request, 'New SMS verification code sent.')

    return redirect('accounts:verify')


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('core:index')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(
                    request,
                    username=user_obj.username,
                    password=password
                )
            except User.DoesNotExist:
                user = authenticate(
                    request,
                    username=username,
                    password=password
                )

            if user:
                if not user.is_active:
                    messages.error(request, 'Please verify your account first.')
                    return redirect('accounts:login')

                login(request, user)
                messages.success(
                    request,
                    f'Welcome back, {user.get_full_name() or user.username}!'
                )
                return redirect(request.GET.get('next', 'core:index'))

            messages.error(request, 'Invalid email/username or password.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

@login_required
def resend_code(request):
    user = request.user

    if user.is_verified:
        messages.info(request, "Your account is already verified.")
        return redirect("core:index")

    send_verification_code(user)

    messages.success(
        request,
        "A new verification code has been sent to your email."
    )

    return redirect("accounts:verify")



@login_required
def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('core:index')


@login_required
def profile_view(request):
    """User profile/dashboard"""
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=user)

    return render(
        request,
        'accounts/profile.html',
        {
            'form': form,
            'user': user
        }
    )
