from django.db import models
from django.contrib.auth.models import AbstractUser
from coreapi.utils.manager import CustomUserManager 

# Create your models here.


#user model
class User(AbstractUser):
    username = None
    email = models.EmailField(unique =True , blank=True , null=True)
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=20)
    phone_number= models.CharField(max_length=50)
    gender = models.CharField(max_length=50)

    type_Choices = (
        ('Tutor' , 'Tutor'),
        ('Learner', 'Learner'),

    )
    type = models.CharField(max_length =20 ,choices =type_Choices, default="Tutor")
    reset_password_token = models.CharField(max_length=255, blank=True, null=True)
    reset_password_token_created_at = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =[]

    def __str__(self):
        if self.first_name and self.second_name: 
            return f"{self.first_name} {self.second_name} {self.type}"
        else :
            return f'{self.id}'
        

class Subject(models.Model):
    name = models.CharField(max_length=100 )
    def __str__(self):
            return self.name

class Post (models.Model):
    post_code = models.CharField(max_length=50)
    owner = models.ForeignKey(User , on_delete=models.CASCADE,  limit_choices_to={'type': 'Learner'} )
    subject = models.ForeignKey('Subject' , on_delete=models.CASCADE)
    question = models.TextField()
    live_needed = models.BooleanField(default=False)
    answered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)

    #string rep

    def __str__(self):
        if self.owner and self.post_code: 
            return f"{self.question} {self.owner}"
        else :
            return f'{self.id}'
        

class Bid(models.Model):
    post = models.ForeignKey('Post' , on_delete=models.CASCADE)
    tutor = models.ForeignKey(User , on_delete=models.CASCADE,  limit_choices_to={'type': 'Tutor'} )
    credits = models.IntegerField(default=0.00)
    accepted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)

class Resource (models.Model):
    post = models.ForeignKey('Post' , on_delete=models.CASCADE)
    tutor = models.ForeignKey(User , on_delete=models.CASCADE,  limit_choices_to={'type': 'Teacher'} )
    created = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    text_resource = models.TextField()
    #doc resource here
    #meeting link , #youtube links can be attached also


