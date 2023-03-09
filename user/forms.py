
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UserForm (UserCreationForm):
    

    
    email =forms.EmailField( required=True ,label="Email")
    first_name = forms.CharField(max_length=100 ,label="First Name")
    last_name = forms.CharField(max_length=100 , label="Last Name")
    mobile_phone = forms.CharField(max_length=15 , label="mobile phone")
   
    class Meta:
        model=User
        fields = ('first_name', "last_name" ,'username', 'email' , 'mobile_phone' , 'password1','password2')

  # First name
  # - Last name
  # - Email
  # - Password
  # - Confirm password
  # - Mobile phone [validated against Egyptian phone
  # numbers]
  # - Profile Picture




