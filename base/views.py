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



# def signup(request):  
     

#     return render(request, 'signup.html', {
#         'title_choices': TITLE_CHOICES,
#         'gender_choices': GENDER_CHOICES,
#         'relationship_status_choices': RELATIONSHIP_STATUS_CHOICES,
#         'countries': countries,
#         'employment_status_choices': EMPLOYMENT_STATUS_CHOICES,
#         'interest_choices': INTEREST_CHOICES,
#         'members': CustomUser.objects.filter(is_memeber=True),   
#     })


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



logger = logging.getLogger(__name__)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.contrib.auth.models import User


def signup(request):
    if request.method == 'POST':
        try:
            # Extract data from POST request
            title = request.POST.get('title')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            gender = request.POST.get('gender')
            date_of_birth = request.POST.get('date_of_birth')
            nationality = request.POST.get('nationality')
            additional_nationality = request.POST.get('additional_nationality')
            relationship_status = request.POST.get('relationship_status')
            address_line = request.POST.get('address_line')
            town_city = request.POST.get('town_city')
            country = request.POST.get('country')
            zipcode = request.POST.get('zipcode')
            state = request.POST.get('state')
            primary_email = request.POST.get('primary_email')
            secondary_email = request.POST.get('secondary_email')
            primary_phone = request.POST.get('primary_phone')
            secondary_phone = request.POST.get('secondary_phone')
            employment_status = request.POST.get('employment_status')
            member_of_club = request.POST.get('member_of_club')
            social_media_platform = request.POST.get('social_media_platform')
            password = request.POST.get('password')
            password1 = request.POST.get('password1')

            # Check for missing fields
            required_fields = [
                title, first_name, last_name, gender, date_of_birth, nationality, 
                additional_nationality, relationship_status, address_line, town_city, 
                country, zipcode, state, primary_email, secondary_email, primary_phone, 
                secondary_phone, employment_status, member_of_club, social_media_platform, 
                password, password1
            ]
            
            missing_fields = [field for field in required_fields if not field]
            missing_fields = [str(field) for field in missing_fields if field]  # Ensure it's a string

            if missing_fields:
                return JsonResponse({"success": False, "errors": f"Missing fields: {', '.join(missing_fields)}"}, status=400)

            # Validate password
            if password != password1:
                return JsonResponse({"success": False, "errors": "Passwords do not match."}, status=400)

            # Handle file uploads
            profile_picture = request.FILES.get('profile_picture')
            id_proof = request.FILES.get('id_proof')

            # Save files if provided
            profile_picture_path = default_storage.save(profile_picture.name, profile_picture) if profile_picture else None
            id_proof_path = default_storage.save(id_proof.name, id_proof) if id_proof else None

            # Create user
            user = CustomUser.objects.create(
                title=title,
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                date_of_birth=date_of_birth,
                nationality=nationality,
                additional_nationality=additional_nationality,
                relationship_status=relationship_status,
                address_line=address_line,
                town_city=town_city,
                country=country,
                zipcode=zipcode,
                state=state,
                primary_email=primary_email,
                email=primary_email,
                username = primary_email,
                secondary_email=secondary_email,
                primary_phone=primary_phone,
                secondary_phone=secondary_phone,
                employment_status=employment_status,
                member_of_club=member_of_club,
                social_media_platform=social_media_platform,
                profile_picture=profile_picture_path,
                proof_of_id=id_proof_path
            )
            user.set_password(password)  # Hash the password before saving
            user.save()


            return redirect("login")

        except Exception as e:
            return JsonResponse({"success": False, "errors": str(e)}, status=500)

    return render(request, 'signup.html', {
        'title_choices': TITLE_CHOICES,
        'gender_choices': GENDER_CHOICES,
        'relationship_status_choices': RELATIONSHIP_STATUS_CHOICES,
        'countries': countries,
        'employment_status_choices': EMPLOYMENT_STATUS_CHOICES,
        'interest_choices': INTEREST_CHOICES,
        'members': CustomUser.objects.filter(is_memeber=True),   
    })


def member(request):
    context = {
        'members': CustomUser.objects.filter(is_memeber=True), 
    }
    return render (request ,'member.html', context)


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

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from stream_chat import StreamChat
from django.conf import settings
import json
import re

User = get_user_model()
client = StreamChat(api_key=settings.STREAM_API_KEY, api_secret=settings.STREAM_API_SECRET)

def format_username(username):
    """Ensure usernames are valid for Stream Chat by replacing invalid characters."""
    return re.sub(r"[^a-zA-Z0-9@_-]", "_", username)

@csrf_exempt
def send_message(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            receiver_username = data.get("receiver")
            message_text = data.get("message")

            if not receiver_username or not message_text:
                return JsonResponse({"error": "Receiver and message are required"}, status=400)

            sender = request.user
            receiver = User.objects.get(username=receiver_username)

            # Format usernames for Stream Chat
            sender_stream_id = format_username(sender.username)
            receiver_stream_id = format_username(receiver.username)

            # Ensure users exist in Stream Chat
            client.upsert_user({"id": sender_stream_id, "name": sender.username})
            client.upsert_user({"id": receiver_stream_id, "name": receiver.username})

            # Create a unique channel for the two users
            channel_id = f"chat_{min(sender.id, receiver.id)}_{max(sender.id, receiver.id)}"
            channel = client.channel("messaging", channel_id, {"members": [sender_stream_id, receiver_stream_id]})
            channel.create(sender_stream_id)

            # Send the message via Stream Chat API
            response = channel.send_message({"text": message_text}, sender_stream_id)

            # Save the message in the database
            ChatMessage.objects.create(sender=sender, receiver=receiver, message=message_text)

            return JsonResponse({"status": "success", "message": response}, status=200)

        except User.DoesNotExist:
            return JsonResponse({"error": "Receiver not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
def get_messages(request, receiver_username):
    sender = request.user
    receiver = CustomUser.objects.get(username=receiver_username)

    messages = ChatMessage.objects.filter(
        sender__in=[sender, receiver], receiver__in=[sender, receiver]
    ).order_by("timestamp")

    messages_data = [{"sender": msg.sender.username, "message": msg.message} for msg in messages]

    return JsonResponse({"messages": messages_data})



def chat_page(request):
    return render(request, "chat.html")

def asklist(request):
    ask = Ask.objects.all()
    context = {
        'ask':ask
    }
    return render (request,'ask.html',context)

def askapi(request):
    if request.method == "POST":
        try:
            data =json.loads(request.body)
            add_title =data.get('add_title')
            discription = data.get('discription')
            date = data.get('date')
            Ask.objects.create(add_title=add_title,discription=discription, date=date,user=request.user)
            return  JsonResponse({'sucess':True},status=200)
        except json.JSONDecodeError:
            return JsonResponse({
            'error':'invalid json',
        },status=400)
    
    return JsonResponse({
            'error':'invalid json',
        },status=405)


def get_users(request):
    User = get_user_model()
    users = User.objects.exclude(username=request.user.username).values_list("username", flat=True)
    return JsonResponse({"users": list(users)})


def eventlist(request):
    return render(request, 'eventlist.html')