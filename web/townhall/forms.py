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
from django.forms import EmailField, CharField

from models import AppUser, UserPost
from django import forms


class UserRegistration(forms.ModelForm):
    password = CharField(widget=forms.PasswordInput)

    class Meta:
        model = AppUser
        fields = ['first_name', 'last_name', 'email', 'password']


class UserLogin(forms.Form):
    password = CharField(widget=forms.PasswordInput)
    email = EmailField(max_length=255)

    # class Meta:
    #     model = AppUser
    #     fields = ['email', 'password']


class UserFormPost(forms.Form):
    title = CharField(max_length=255)
    summary = CharField(widget=forms.Textarea)
    description = CharField(widget=forms.Textarea)
    city = CharField(max_length=255)
    state = CharField(max_length=255)
    zipcode = CharField(max_length=255)
    # class Meta:
    #     model = UserPost
    #     fields = ['title', 'description']
