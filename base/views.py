from django.shortcuts import render ,get_object_or_404 
from .models import *
from django.contrib import auth
from django.http import JsonResponse
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
from .models import ReferralRequest

CustomUser = get_user_model()



def signup(request):
    if request.method == "POST":
        # Collect form data
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
        primary_email = request.POST.get('primary_email').strip().lower()
        secondary_email = request.POST.get('secondary_email')
        primary_phone = request.POST.get('primary_phone')
        secondary_phone = request.POST.get('secondary_phone')
        employment_status = request.POST.get('employment_status')
        interests = request.POST.getlist('interests')
        member_of_club = request.POST.get('member_of_club')
        social_media_platform = request.POST.get('social_media_platform')
        proof_of_id = request.FILES.get('proof_of_id')
        profile_picture = request.FILES.get('profile_picture')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        selected_referrals = request.POST.getlist('referrals')

        errors = {}

        # Validate required fields
        required_fields = {
            'title': title, 'first_name': first_name, 'last_name': last_name, 'gender': gender, 
            'date_of_birth': date_of_birth, 'nationality': nationality, 'relationship_status': relationship_status, 
            'address_line': address_line, 'town_city': town_city, 'country': country, 'zipcode': zipcode, 
            'primary_email': primary_email, 'primary_phone': primary_phone, 'employment_status': employment_status, 
            'interests': interests, 'member_of_club': member_of_club, 'social_media_platform': social_media_platform, 
            'proof_of_id': proof_of_id, 'profile_picture': profile_picture, 'password': password, 'password1': password1
        }

        for field, value in required_fields.items():
            if not value:
                errors[field] = f"{field.replace('_', ' ').capitalize()} is required."

        # Validate email uniqueness
        if CustomUser.objects.filter(email=primary_email).exists():
            errors['primary_email'] = "An account with this email already exists."

        # Validate phone uniqueness
        if CustomUser.objects.filter(primary_phone=primary_phone).exists():
            errors['primary_phone'] = "This phone number is already in use."

        # Validate password match
        if password != password1:
            errors['password1'] = "Passwords do not match."

        # Ensure passwords meet security standards
        if len(password) < 8:
            errors['password'] = "Password must be at least 8 characters long."

        if not any(char.isdigit() for char in password):
            errors['password'] = "Password must contain at least one number."

        if not any(char.isalpha() for char in password):
            errors['password'] = "Password must contain at least one letter."

        # Ensure exactly 3 referrals are selected
        if len(selected_referrals) != 3:
            errors['referrals'] = "You must select exactly 3 members to support your registration."

        # Validate referrals
        selected_members = CustomUser.objects.filter(id__in=selected_referrals)
        if len(selected_members) != 3:
            errors['referrals'] = "Invalid referral selection."

        # If there are any errors, return them to the form
        if errors:
            return render(request, 'signup.html', {
                'errors': errors,
                'title_choices': TITLE_CHOICES,
                'gender_choices': GENDER_CHOICES,
                'relationship_status_choices': RELATIONSHIP_STATUS_CHOICES,
                'countries': countries,
                'employment_status_choices': EMPLOYMENT_STATUS_CHOICES,
                'interest_choices': INTEREST_CHOICES,
                'members': CustomUser.objects.all(),  
            })

        # Create user
        user = CustomUser(
            username=primary_email,
            email=primary_email,
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
            proof_of_id=proof_of_id,
            profile_picture=profile_picture,
            state=state,
            secondary_email=secondary_email
        )

        # Set password securely and save user
        user.set_password(password)
        user.save()

        # Create referral requests
        for member in selected_members:
            ReferralRequest.objects.create(
                referred_user=user,
                referring_user=member,
                approved=False  # Pending approval
            )

        messages.success(request, "Registration successful! Please wait for approval from your referrals.")
        return render(request, 'signup.html', {
            'success': "Your registration has been submitted successfully!",
            'title_choices': TITLE_CHOICES,
            'gender_choices': GENDER_CHOICES,
            'relationship_status_choices': RELATIONSHIP_STATUS_CHOICES,
            'countries': countries,
            'employment_status_choices': EMPLOYMENT_STATUS_CHOICES,
            'interest_choices': INTEREST_CHOICES,
            'members': CustomUser.objects.all(),  
        })

    return render(request, 'signup.html', {
        'title_choices': TITLE_CHOICES,
        'gender_choices': GENDER_CHOICES,
        'relationship_status_choices': RELATIONSHIP_STATUS_CHOICES,
        'countries': countries,
        'employment_status_choices': EMPLOYMENT_STATUS_CHOICES,
        'interest_choices': INTEREST_CHOICES,
        'members': CustomUser.objects.all(),  
    })


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid email or password.")
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