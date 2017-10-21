# from django.contrib.auth.forms import UserCreationForm
#
# from models import AppUser
#
#
# class CustomerAppUserRegistrationForm(UserCreationForm):
#     def __init__(self, *args, **kargs):
#         super(CustomerAppUserRegistrationForm, self).__init__(*args, **kargs)
#         del self.fields['username']
#
#     class Meta:
#         model = AppUser
#         fields = {"email", }

# from django.contrib.auth.models import User
from models import AppUser
from django import forms


class UserRegistration(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = AppUser
        fields = ['email', 'password']

    # print()