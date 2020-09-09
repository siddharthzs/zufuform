from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Create your models here.



class RegisterForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username','password1','password2']