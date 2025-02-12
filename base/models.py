from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


  

class CustomUser(AbstractUser):
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

    title = models.CharField(max_length=10, choices=TITLE_CHOICES, blank=True)
    
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(blank=True,null=True)
    nationality = models.CharField(max_length=100)
    additional_nationality = models.CharField(max_length=100, blank=True, null=True)
    relationship_status = models.CharField(max_length=20, choices=RELATIONSHIP_STATUS_CHOICES)
    
    # Address
    address_line = models.CharField(max_length=255)
    town_city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    
    # Contact Details
    primary_email = models.EmailField(unique=True)
    secondary_email = models.EmailField(blank=True, null=True)
    primary_phone = models.CharField(max_length=20)
    secondary_phone = models.CharField(max_length=20, blank=True, null=True)

    # Employment & Interests
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS_CHOICES)
    interests = models.CharField(max_length=255, default="Travel, Sports, Reading")  # Default random interests
    
    # Club Membership & Social Media
    member_of_club = models.CharField(max_length=255, blank=True, null=True)
    social_media_platform = models.CharField(max_length=255, blank=True, null=True)
    
    # Uploads
    proof_of_id = models.ImageField(upload_to='uploads/ids/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='uploads/profile_pics/', blank=True, null=True)

    # # Referrals (User selects 3 existing members to approve them)
    # referrals = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='referred_users')

    def __str__(self):
        return f"{self.username} {self.last_name} ({self.primary_email})"

