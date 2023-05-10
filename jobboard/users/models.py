from django.db import models
from django.conf import settings
#from django.contrib.auth.models import User
# Create your models here.
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from ckeditor.fields import RichTextField

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, **extra_fields):
        #mobile attr removed fromt the function argument
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError("Password is not provided")
        
        user = self.model(
        email = self.normalize_email(email),
        first_name = first_name,
        last_name = last_name,
        #mobile = mobile,
        *extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    #mobile attr removed fromt the function argument
    def create_user(self, email, password, first_name, last_name,  **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active' ,True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, first_name, last_name, password, **extra_fields)
        #mobile attr removed fromt the return stmt
    
    #mobile attr removed fromt the function argument
    def create_superuser(self, email, password, first_name, last_name,  **extra_fields):
        extra_fields.setdefault( 'is_staff', True)
        extra_fields.setdefault('is_active',  True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, first_name, last_name,  **extra_fields)
        #mobile attr removed fromt the return stmt



class User (AbstractBaseUser, PermissionsMixin):
    # Abstractbaseuser has password, last_login, is_active by default

    email = models.EmailField(db_index=True, unique=True, max_length=254)
    first_name = models.CharField(max_length=240)
    last_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=50)
    address = models.CharField( max_length=250)
    
    is_staff = models.BooleanField(default=True) # must needed, otherwise you
    is_active = models.BooleanField(default=True) # must needed, otherwise yo
    is_superuser = models.BooleanField(default=False) # this field we inherit
    is_employer = models.BooleanField(default=False)
    
    
    
    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['first_name','last_name','mobile']
    #REQUIRED_FIELDS = ['first_name','last_name']
    
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users' 



class Applicant(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    image = models.ImageField(upload_to="profileimg")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.CharField(max_length=255)

    # def __str__(self):
    #     return self.user.first_name

class Employer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    address = models.TextField()
    def __str__ (self):
        return self.user.username

class Job(models.Model):
    CITY_CHOICES = [
        ('Pune', 'Pune'),
        ('Mumbai', 'Mumbai'),
        ('Delhi', 'Delhi'),
        ('Bangalore', 'Bangalore'),
        ('Hyderabad', 'Hyderabad'),
        ('Chennai', 'Chennai'),
        ('Kolkata', 'Kolkata'),
    ]

    JOB_TYPE_CHOICES = [
        ('technology', 'Technology'),
        ('finance', 'Finance'),        
        ('healthcare', 'Healthcare'),        
        ('education', 'Education'),        
        ('manufacturing', 'Manufacturing'),   
    ]

    STATUS_CHOICES = [
        (True, 'Published'),
        (False, 'Disabled')
    ]

    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to='job_images')
    email = models.EmailField()
    job_title = models.CharField(max_length=100)
    location = models.CharField(max_length=50, choices=CITY_CHOICES)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    job_description = RichTextField(blank=True, null=True)
    company_name = models.CharField(max_length=100)
    company_description = RichTextField(blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos')
    last_date_of_application = models.DateField(default=timezone.now)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    salary_min = models.PositiveIntegerField(null=True, blank=True)
    salary_max = models.PositiveIntegerField(null=True, blank=True)
    experience_min = models.PositiveIntegerField(null=True, blank=True)
    experience_max = models.PositiveIntegerField(null=True, blank=True)
    status = models.BooleanField(choices=STATUS_CHOICES, default=True)
    
    def __str__(self):
        return self.job_title
    


class JobApplication(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    address = models.TextField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    #passport_photo = models.ImageField(upload_to='passport_photos/')
    email = models.EmailField()
    phone_no = models.CharField(max_length=15)
    linkedin = models.URLField()
    portfolio_links = models.URLField(blank=True)
