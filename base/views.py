from django.shortcuts import render ,get_object_or_404 
from .models import *
from django.contrib import auth
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    events = Event.objects.all()
    return render(request, 'index.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event_data = {
        'id': event.id,
        'name': event.name,
        'description': event.description,
        'date': event.time,  # Format date
        'location': event.location,
        'image': event.image.url if event.image else None
    }
    return JsonResponse(event_data)


from django.shortcuts import render, redirect
from django_countries import countries  # Import Django Countries

# Define choices
TITLE_CHOICES = [
    ('Mr', 'Mr'),
    ('Mrs', 'Mrs'),
    ('Miss', 'Miss'),
    ('Dr', 'Dr'),
    ('Prof', 'Prof'),
]

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

RELATIONSHIP_STATUS_CHOICES = [
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Divorced', 'Divorced'),
    ('Widowed', 'Widowed'),
]
EMPLOYMENT_STATUS_CHOICES = [
        ('Employed', 'Employed'),
        ('Self-employed', 'Self-employed'),
        ('Unemployed', 'Unemployed'),
        ('Student', 'Student'),
        ('Retired', 'Retired'),
    ]
INTEREST_CHOICES = [
    ('sports', 'Sports'),
    ('music', 'Music'),
    ('travel', 'Travel'),
    ('technology', 'Technology'),
    ('art', 'Art'),
    ('gaming', 'Gaming'),
    ('fitness', 'Fitness'),
    ('business', 'Business'),
    ('science', 'Science'),
    ('fashion', 'Fashion'),
]


from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib import messages
from django_countries import countries


CustomUser = get_user_model()



def signup(request):  
     

    return render(request, 'signup.html', {
        'title_choices': TITLE_CHOICES,
        'gender_choices': GENDER_CHOICES,
        'relationship_status_choices': RELATIONSHIP_STATUS_CHOICES,
        'countries': countries,
        'employment_status_choices': EMPLOYMENT_STATUS_CHOICES,
        'interest_choices': INTEREST_CHOICES,
        'members': CustomUser.objects.filter(is_memeber=True),   
    })


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from .models import CustomUser

# Setup logging
logger = logging.getLogger(__name__)

@csrf_exempt
def signupx(request):
    if request.method == "POST":
        try:
            # Decode request body safely
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError as e:
            logger.error(f"JSON Decode Error: {str(e)}")
            return JsonResponse({'success': False, 'error': 'Invalid JSON format'}, status=400)

        try:
            # Extracting user details
            title = data.get('title')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            gender = data.get('gender')
            date_of_birth = data.get('date_of_birth')
            nationality = data.get('nationality')
            additional_nationality = data.get('additional_nationality')
            relationship_status = data.get('relationship_status')
            address_line = data.get('address_line')
            town_city = data.get('town_city')
            country = data.get('country')
            zipcode = data.get('zipcode')
            state = data.get('state')
            primary_email = data.get('primary_email', '').strip().lower()
            secondary_email = data.get('secondary_email')
            primary_phone = data.get('primary_phone')
            secondary_phone = data.get('secondary_phone')
            employment_status = data.get('employment_status')
            interests = data.get('interests', [])
            member_of_club = data.get('member_of_club')
            social_media_platform = data.get('social_media_platform')
            password = data.get('password')
            password1 = data.get('password1')

            errors = {}

            required_fields = {
                'title': title, 'first_name': first_name, 'last_name': last_name, 'gender': gender, 
                'date_of_birth': date_of_birth, 'nationality': nationality, 'relationship_status': relationship_status, 
                'address_line': address_line, 'town_city': town_city, 'state':state, 'country': country, 'zipcode': zipcode, 
                'primary_email': primary_email, 'employment_status': employment_status, 
                'member_of_club': member_of_club, 'social_media_platform': social_media_platform, 
                'password': password, 'password1': password1
            }

            # Check required fields
            for field, value in required_fields.items():
                if not value:
                    errors[field] = f"{field.replace('_', ' ').capitalize()} is required."

            # Check for duplicate email
            if CustomUser.objects.filter(email=primary_email).exists():
                errors['primary_email'] = "An account with this email already exists."

            # Password validation
            if password != password1:
                errors['password1'] = "Passwords do not match."

            if len(password) < 8:
                errors['password'] = "Password must be at least 8 characters long."

            if not any(char.isdigit() for char in password):
                errors['password'] = "Password must contain at least one number."

            if not any(char.isalpha() for char in password):
                errors['password'] = "Password must contain at least one letter."

            # Return errors if found
            if errors:
                return JsonResponse({'success': False, 'errors': errors}, status=400)

            # Create the user
            user = CustomUser(
                username=primary_email,
                email=primary_email,
                primary_email= primary_email,
                first_name=first_name,
                last_name=last_name,
                title=title,
                gender=gender,
                date_of_birth=date_of_birth,
                nationality=nationality,
                additional_nationality=additional_nationality,
                relationship_status=relationship_status,
                address_line=address_line,
                town_city=town_city,
                country=country,
                zipcode=zipcode,
                primary_phone=primary_phone,
                secondary_phone=secondary_phone,
                employment_status=employment_status,
                member_of_club=member_of_club,
                social_media_platform=social_media_platform,
                state=state,
                secondary_email=secondary_email
            )

            user.set_password(password)
            user.save()

            return JsonResponse({'success': True, 'message': "Registration successful! Please wait for approval from your referrals."}, status=201)

        except IntegrityError as e:
            logger.error(f"Database Integrity Error: {str(e)}")
            return JsonResponse({'success': False, 'error': 'A database error occurred. Please try again.'}, status=500)

        except Exception as e:
            logger.error(f"Unexpected Error: {str(e)}")
            return JsonResponse({'success': False, 'error': 'An unexpected error occurred. Please contact support.'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json



import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
  # Import DeclinedReferral model

CustomUser = get_user_model()

@csrf_exempt
def send_referrals(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            sender_id = data.get('sender_id')
            selected_users = data.get('selected_users', [])

            if not sender_id or len(selected_users) != 3:
                return JsonResponse({'success': False, 'error': "You must select exactly 3 members."}, status=400)

            sender = CustomUser.objects.get(id=sender_id)
            existing_referrals = Referral.objects.filter(sender=sender)

            if existing_referrals.count() == 0:
                # If no referrals exist, create new ones
                for receiver_id in selected_users:
                    receiver = CustomUser.objects.get(id=receiver_id)
                    Referral.objects.create(sender=sender, receiver=receiver)

            elif existing_referrals.count() == 3:
                # If exactly 3 exist, update them
                for referral, new_receiver_id in zip(existing_referrals, selected_users):
                    new_receiver = CustomUser.objects.get(id=new_receiver_id)

                    if referral.accepted is False:  # If the referral was declined
                        DeclinedReferral.objects.create(sender=sender, receiver=referral.receiver)

                    referral.receiver = new_receiver  # Update receiver
                    referral.accepted = None  # Reset status to pending
                    referral.save()

            else:
                return JsonResponse({'success': False, 'error': "Invalid number of existing referrals. Contact support."}, status=400)

            return JsonResponse({'success': True, 'message': "Referrals updated successfully!"}, status=200)

        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'error': "User not found."}, status=404)

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def status(request):
    user = request.user  # Get the logged-in user

    # Count the number of declined referrals
    declined_count = DeclinedReferral.objects.filter(sender=user).count()

    if declined_count >= 3:
        # Delete only the three Referral objects associated with the user
        Referral.objects.filter(sender=user).delete()

        # Get the declined referrals to display
        declined_referrals = DeclinedReferral.objects.filter(sender=user)

        context = {"status": "declined", "declined_referrals": declined_referrals}
    else:
        # Get active referrals if the user has not been blocked
        sent_referrals = Referral.objects.filter(sender=user).select_related('receiver')

        context = {"referrals": sent_referrals, "status": None}

    return render(request, 'status-page.html', context)

@login_required(login_url='login')
def check_referral_status(request):
    user = request.user
    declined_count = Referral.objects.filter(sender=user, accepted=False).count()

    if declined_count >= 3:
        return JsonResponse({"status": "blocked", "message": "Please wait for 6 months before you log in."})

    if 1 <= declined_count < 3:
        return JsonResponse({"status": "pending", "message": "You need to add other referrals."})
    if declined_count >= 0:
        return JsonResponse({"status": "good", "message": "Still Pending."})
    

    return JsonResponse({"status": "allowed"})



@login_required(login_url='login')
def check_declined_referrals(request):
    user = request.user
    declined_count = DeclinedReferral.objects.filter(sender=user).count()

    if declined_count >= 3:
        return JsonResponse({"status": "blocked", "message": "Please wait for 6 months before you log in."})

    return JsonResponse({"status": "allowed"})



def check_referral_approval(request):
    user = request.user  # Get the logged-in user

    # Get all referrals associated with the user
    approved_count = Referral.objects.filter(sender=user, accepted=True).count()

    if approved_count == 3:
        return JsonResponse({"status": "approved", "redirect_url": "/payment/"})  # Redirect to payment
    else:
        return JsonResponse({"status": "pending"})
    
def payment(request):
    return render (request, 'payment.html')



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Referral

@login_required(login_url='login')
def add_referral(request):
    user = request.user  # Get logged-in user

    # Get users the sender has referred (excluding declined ones)
    sent_referrals = Referral.objects.filter(sender=user).exclude(accepted=False)

    # Extract the user IDs of pending/approved referrals
    checked_member_ids = sent_referrals.values_list('receiver_id', flat=True)

    # Get all eligible members (exclude those already declined)
    all_members = CustomUser.objects.exclude(id__in=Referral.objects.filter(sender=user, accepted=False).values_list('receiver_id', flat=True))

    return render(request, "add_referral.html", {
        "members": all_members,
        "checked_members": list(checked_member_ids)
    })




def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            
            # Check if the sender has approved referrals
            payment = Payment.objects.filter(user=user, status='Completed').exists()
            approved_count = Referral.objects.filter(sender=user, accepted=True).count()
            if payment:
               return redirect('index')  #
            if approved_count >= 3:
                return redirect('payment')  # Redirect to payment page if approved referrals exist
            else:
                return redirect('status')  # Redirect to status page if no approved referral
            
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')
    
    return render(request, 'login.html')

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.conf import settings

from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from smtplib import SMTPException


def forget(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"{request.scheme}://{request.get_host()}/reset-password/{uid}/{token}/"

            try:
                send_mail(
                    'Reset Your Password',
                    f"Hi {user.username},\n\nUse the link below to reset your password:\n{reset_link}\n\nIf you didn't request this, please ignore this email.",
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'A password reset link has been sent to your email.')
            except SMTPException as e:
                messages.error(request, f"Email could not be sent. Error: {e}")
                return redirect('forget')

        except CustomUser.DoesNotExist:
            messages.error(request, 'No account found with this email.')
        except BadHeaderError:
            messages.error(request, 'Invalid header found in email.')

        return redirect('forget')
    return render(request, 'forget.html')

from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib import messages

CustomUser = get_user_model()

def reset_password(request, uidb64, token):
    try:
        # Decode the user ID from the URL
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (CustomUser.DoesNotExist, ValueError, TypeError):
        messages.error(request, "Invalid password reset link.")
        return redirect('forget')  # Redirect to "Forget Password" page

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password and confirm_password:
            if new_password == confirm_password:
                # Validate the token
                if default_token_generator.check_token(user, token):
                    # Save the new password
                    user.password = make_password(new_password)
                    user.save()
                    messages.success(request, "Your password has been reset successfully.")
                    return redirect('login')  # Redirect to login page
                else:
                    messages.error(request, "The password reset link is invalid or has expired.")
            else:
                messages.error(request, "Passwords do not match.")
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'reset_password.html', {'uidb64': uidb64, 'token': token})


# account profile backend code 


from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import CustomUser

def AccountProfile(request):
    userprofile = get_object_or_404(CustomUser, email=request.user.email)

    if request.method == "POST":
        userprofile.first_name = request.POST.get('first_name')
        userprofile.gender = request.POST.get('gender')
        userprofile.email = request.POST.get('email')
        userprofile.date_of_birth = request.POST.get('date_of_birth')
        userprofile.primary_phone = request.POST.get('primary_phone')
        userprofile.country = request.POST.get('country')
        
        userprofile.save()  # Save the updated profile

        messages.success(request, "Profile updated successfully!")

    return render(request, 'account.html', {'userprofile': userprofile})




# def approve_referral(request, referral_id):
#     referral = ReferralRequest.objects.get(id=referral_id, referring_user=request.user)

#     if referral:
#         referral.approved = True
#         referral.save()

#         # Check if all three referrals are approved
#         referred_user = referral.referred_user
#         if referred_user.incoming_requests.filter(approved=True).count() >= 3:
#             referred_user.referral_approved = True
#             referred_user.save()

#         return redirect('dashboard')  # Redirect after approval

#     return redirect('error_page')  # Handle invalid cases
from django.http import JsonResponse
from stream_chat import StreamChat
from django.conf import settings

# Initialize Stream Client
client = StreamChat(api_key=settings.STREAM_API_KEY, api_secret=settings.STREAM_API_SECRET)

# Function to generate a user token
def get_token(request):
    user_id = request.GET.get("user_id")
    token = client.create_token(user_id)
    return JsonResponse({"token": token, "api_key": settings.STREAM_API_KEY})


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from stream_chat import StreamChat
from django.conf import settings



@csrf_exempt  # Disable CSRF (Only for testing)
def send_message(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        message = request.POST.get("message")

        if not user_id or not message:
            return JsonResponse({"error": "Missing user_id or message"}, status=400)

        try:
            channel = client.channel("messaging", "general")
            channel.create(user_id)
            response = channel.send_message({"text": message}, user_id)
            return JsonResponse({"status": "success", "message": response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request"}, status=400)




def chat_page(request):
    return render(request, "chat.html")