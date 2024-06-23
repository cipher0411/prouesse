from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from item.models import Category, Item
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import SignupForm, LoginForm, UserUpdateForm, ProfileUpdateForm, PasswordResetRequestForm, SetPasswordForm, AccountDeletionForm
from .models import Profile
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import update_session_auth_hash
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from conversation.models import ConversationMessage
from django.core.exceptions import ObjectDoesNotExist
import random
import logging
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.utils.encoding import force_str
import random
from django.core.exceptions import MultipleObjectsReturned
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Profile, otp_Profile
from django.views import View 
from .forms import ContactForm








logger = logging.getLogger(__name__)

# View profile
@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'core/profile.html', {'profile': profile})



@login_required
def profile_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
        otp_profile = otp_Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)  # Create profile if it doesn't exist
    except otp_Profile.DoesNotExist:
        otp_profile = otp_Profile.objects.create(user=request.user)  # Create otp_profile if it doesn't exist
    
    context = {
        'profile': profile,
        'otp_profile': otp_profile,
    }
    return render(request, 'core/profile.html', context)



# Update user profile information
@login_required
def update_user(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            user = u_form.save(commit=False)
            password = u_form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()

            p_form = ProfileUpdateForm(request.POST, instance=profile)
            if p_form.is_valid():
                p_form.save()
                messages.success(request, 'Your profile was successfully updated!')
                if password:
                    updated_user = authenticate(username=user.username, password=password)
                    if updated_user is not None:
                        login(request, updated_user)
                        update_session_auth_hash(request, user)
                return redirect('core:profile')
            else:
                messages.error(request, 'There was an error updating your profile. Please correct the errors below.')
        else:
            messages.error(request, 'There was an error updating your profile. Please correct the errors below.')
    else:
        u_form = UserUpdateForm(instance=request.user)

    return render(request, 'core/update_user.html', {
        'u_form': u_form,
    })

# Home page
def index(request):
    items = Item.objects.filter(is_sold=False).order_by('-created_at')[:6]
    categories = Category.objects.all()
    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })

# Category items page
def category_items(request, category_id):
    category_obj = get_object_or_404(Category, pk=category_id)
    items = Item.objects.filter(category_id=category_id, is_sold=False)
    return render(request, 'core/category_items.html', {
        'category': category_obj,
        'items': items,
    })

def faq_view(request):
    return render(request, 'core/faq.html')

# Contact page
def contact(request):
    return render(request, 'core/contact.html')

# Student portal page

def student_portal(request):
    return render(request, 'core/student_portal.html')

# Student practical page

def student_practical(request):
    return render(request, 'core/student_practical.html')

# About page
def about(request):
    return render(request, 'core/about.html')

# Gallery page
def gallery(request):
    return render(request, 'core/gallery.html')

# Ready to wear page
def ready_to_wear(request):
    return render(request, 'core/ready_to_wear.html')

# Ebook page
def ebook(request):
    return render(request, 'core/ebook.html')

# Training page
def training(request):
    return render(request, 'core/training.html')

# Custom made page
def custom_made(request):
    return render(request, 'core/custom_made.html')

# Courses page

def courses(request):
    return render(request, 'core/courses.html')

# Market place page
def market_place(request):
    return render(request, 'core/market_place.html')




# User login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.user
            try:
                profile = user.profile
                login(request, user)
                messages.info(request, f"You are now logged in as {user.username}.")
                return redirect('core:index')
            except ObjectDoesNotExist:
                messages.error(request, "User has no profile.")
                return redirect('core:signup')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})





def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['terms_accepted']:
                user = form.save()
                # Assuming Profile and Profile.objects.filter(user=user) exist
                if not Profile.objects.filter(user=user).exists():
                    Profile.objects.create(user=user)

                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                if user:
                    login(request, user)
                    messages.success(request, 'You have successfully created an account and logged in!')
                    return redirect('core:index')
                else:
                    messages.error(request, 'Invalid username or password after signup.')
                    return redirect('core:signup')
            else:
                # Redirect to terms and conditions view if terms are not accepted
                return redirect('core:terms_and_conditions')
    else:
        form = SignupForm()
    
    return render(request, 'core/signup.html', {'form': form})

def terms_and_conditions_view(request):
    return render(request, 'core/terms_and_conditions.html')










# User logout
@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('core:index')

# Delete account page
@login_required
def delete_account(request):
    if request.method == 'POST':
        form = AccountDeletionForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason_for_deletion']
            send_account_deletion_email(request.user.email, reason)

            user = request.user
            logout(request)
            user.delete()

            messages.success(request, 'Your account has been deleted successfully.')
            return redirect('core:index')
    else:
        form = AccountDeletionForm()

    return render(request, 'core/account_delete.html', {'form': form})



# Send account deletion email
def send_account_deletion_email(email, reason):
    subject = 'Account Deletion Request'
    html_message = render_to_string('core/account_deletion_email.html', {'reason': reason})
    plain_message = strip_tags(html_message)

    try:
        send_mail(subject, plain_message, 'uwajohn101@gmail.com', [email], html_message=html_message)
        logger.info(f"Account deletion email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send account deletion email to {email}: {e}")








def cookies_view(request):
    return render(request, 'core/cookies.html')






class ForgotPasswordView(View):
    def get(self, request):
        # Clear the session if it exists
        if 'email' in request.session:
            del request.session['email']
        return render(request, 'core/forgot_password.html')

    def post(self, request):
        try:
            email = request.POST.get('email')
            user = User.objects.get(email=email)
            otp_profile, created = otp_Profile.objects.get_or_create(user=user)
            
            # Generate OTP and set its expiration time
            otp = random.randint(100000, 999999)
            otp_profile.otp = otp
            otp_profile.otp_created_at = timezone.now()
            otp_profile.save()
            
            # Send OTP via email
            send_mail(
                'Password Reset OTP',
                f'Your OTP for password reset is {otp}. This OTP is valid for 5 minutes.',
                'support@prouessefashion.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, f'OTP sent successfully to {email}.')
            request.session['email'] = email  # Store the email in session for verification
            return redirect('core:verify_otp')  # Use the correct namespace here
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('core:forgot_password')  # Use the correct namespace here
        except Exception as e:
            messages.error(request, f'Failed to send OTP. Error: {e}')
            return redirect('core:forgot_password')  # Use the correct namespace here


class VerifyOTPView(View):
    def get(self, request):
        return render(request, 'core/verify_otp.html')

    def post(self, request):
        otp = request.POST.get('otp')
        email = request.session.get('email')
        if not email:
            return redirect('core:forgot_password')
        try:
            user = User.objects.get(email=email)
            otp_profile = otp_Profile.objects.get(user=user)
            if otp_profile.otp == int(otp) and otp_profile.is_otp_valid():
                # OTP is valid, proceed to reset password
                request.session['otp_verified'] = True  # Mark OTP as verified
                return redirect('core:reset_password')
            else:
                if not otp_profile.is_otp_valid():
                    messages.error(request, 'OTP has expired. Please request a new OTP.')
                else:
                    messages.error(request, 'Invalid OTP')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
        except otp_Profile.DoesNotExist:
            messages.error(request, 'OTP profile does not exist for this user.')
        except otp_Profile.RelatedObjectDoesNotExist:
            messages.error(request, 'OTP profile does not exist for this user.')
        
        return redirect('core:verify_otp')  # Use the correct namespace here


class ResetPasswordView(View):
    def get(self, request):
        # Check if OTP was verified
        if not request.session.get('otp_verified'):
            return redirect('core:forgot_password')
        return render(request, 'core/reset_password.html')

    def post(self, request):
        email = request.session.get('email')
        if not email:
            return redirect('core:forgot_password')
        try:
            user = User.objects.get(email=email)
            password = request.POST['password']
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful.')
            
            # Clear the session email and otp_verified after successful password reset
            del request.session['email']
            del request.session['otp_verified']
            return redirect('core:login')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
        
        return redirect('core:forgot_password')
    
    
    
def test_email(request):
    try:
        send_mail(
            'Test Email',
            'This is a test email.',
            'support@cipherknights.com',
            ['uwajohn101@outlook.com'],
            fail_silently=False,
        )
        return HttpResponse("Email sent successfully.")
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    






def contact(request):
    if request.method == 'POST':
        # Extract data from POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        service = request.POST.get('service')
        message = request.POST.get('message')

        # Perform basic validation (you can add more validation as needed)
        if not name or not email or not message:
            messages.error(request, 'Please fill in all required fields.')
        else:
            # Create a new instance of the ContactForm using extracted data
            form = ContactForm({
                'name': name,
                'email': email,
                'phone': phone,
                'service': service,
                'message': message,
            })
            # Save the form if it's valid
            if form.is_valid():
                form.save()
                messages.success(request, 'Your message has been sent successfully, we will get back to you as soon as possible!')
                return redirect('core:contact')  # Redirect to contact page after successful submission
            else:
                messages.error(request, 'Error submitting your message. Please try again.')

    else:
        form = ContactForm()  # Create a blank form instance for GET requests

    return render(request, 'core/contact.html', {'form': form})
