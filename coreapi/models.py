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
        ('Tutor' , 'Teacher'),
        ('Learner', 'Learner'),

    )
    type = models.CharField(max_length =20 ,choices =type_Choices, default= "teacher")
    reset_password_token = models.CharField(max_length=255, blank=True, null=True)
    reset_password_token_created_at = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =[]

    def __str__(self):
        if self.first_name and self.last_name: 
            return f"{self.first_name} {self.last_name} {self.type}"
        else :
            return f'{self.id}'
