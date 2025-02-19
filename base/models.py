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
    state = models.CharField(max_length=100,blank=True, null=True)
    
    # Contact Details
    primary_email = models.EmailField(unique=True)
    secondary_email = models.EmailField(blank=True, null=True)
    primary_phone = models.CharField(max_length=20 , blank=True, null=True)
    secondary_phone = models.CharField(max_length=20, blank=True, null=True)

    # Employment & Interests
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS_CHOICES)
    interests = models.CharField(max_length=100, choices=INTEREST_CHOICES, blank=True) 

    
    # Club Membership & Social Media
    member_of_club = models.CharField(max_length=255, blank=True, null=True)
    social_media_platform = models.CharField(max_length=255, blank=True, null=True)
    
    # Uploads
    proof_of_id = models.ImageField(upload_to='uploads/ids/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='uploads/profile_pics/', blank=True, null=True)

    referrals = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='referred_users')
    is_memeber = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     from django.contrib.auth import get_user_model
    #     User = get_user_model()
        
    #     # If there are no users in the system, allow registration without referrals
    #     if User.objects.count() == 0:
    #         super().save(*args, **kwargs)
    #     else:
    #         if self.referrals.count() < 3:
    #             raise ValueError("You must select at least 3 referrals")
    #         super().save(*args, **kwargs)
  

    def __str__(self):
        return f"{self.username} {self.last_name} "
    

class Referral(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_referrals')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_referrals')
    accepted = models.BooleanField(null=True, blank=True)  # None = Pending, True = Accepted, False = Declined
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({'Accepted' if self.accepted else 'Declined' if self.accepted == False else 'Pending'})"





class DeclinedReferral(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="declined_referrals")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="declined_by")
    declined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} declined by {self.receiver} on {self.declined_at.strftime('%Y-%m-%d %H:%M')}"




class Event(models.Model):
    AUDIENCE_CHOICES = [
        ('public', 'Public'),
        ('members_only', 'Members Only'),
        ('vip', 'VIP')
    ]

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    time = models.DateTimeField()
    description = models.TextField()
    audience_type = models.CharField(max_length=20, choices=AUDIENCE_CHOICES, default='public')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_tickets = models.PositiveIntegerField()
    attending_members = models.ManyToManyField(CustomUser, blank=True)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)

    def __str__(self):
        return self.name



class Ask(models.Model):
    user = models.ForeignKey(CustomUser,  on_delete=models.CASCADE)
    add_title = models.CharField(max_length=50)
    discription =models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.add_title

class Payment(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed')
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"


