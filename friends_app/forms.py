from django import forms
from .models import Friend
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class FriendForm(forms.ModelForm):
    class Meta:
        model = Friend
        fields = ['name', 'phone_number', 'email', 'college', 'address']

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
