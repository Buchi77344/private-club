from django.shortcuts import render
from .models import *
# Create your views here.
def index(request):
    return render (request, 'index.html')


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
from django_countries.data import COUNTRIES
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
                'countries': COUNTRIES,
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
            'countries': COUNTRIES,
            'employment_status_choices': EMPLOYMENT_STATUS_CHOICES,
            'interest_choices': INTEREST_CHOICES,
            'members': CustomUser.objects.all(),  
        })

    return render(request, 'signup.html', {
        'title_choices': TITLE_CHOICES,
        'gender_choices': GENDER_CHOICES,
        'relationship_status_choices': RELATIONSHIP_STATUS_CHOICES,
        'countries': COUNTRIES,
        'employment_status_choices': EMPLOYMENT_STATUS_CHOICES,
        'interest_choices': INTEREST_CHOICES,
        'members': CustomUser.objects.all(),  
    })








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

