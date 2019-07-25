from django import forms
from django.contrib.auth.models import User
from .models import Popsicle, Profile

class PopsicleForm (forms.ModelForm) :
    class Meta :
        model = Popsicle
        fields = ["name", "UPC", "flavor", "popsicle_type", "price",
                  "quantity", "description", "available"]
                  

class ContactForm (forms.Form) :
    name = forms.CharField(max_length = 100, required=True)
    email = forms.EmailField(required=True)
    mobile = forms.CharField(max_length=20, required=True)
    message = forms.CharField(widget = forms.Textarea , help_text = "write your message here")


class ProfileForm (forms.ModelForm) :
    class Meta :
        model = Profile
        fields = ["mobile", "mobileReserve",]


class UserForm (forms.ModelForm) :
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta :
        model = User
        fields = ["username", "email", "password"]

        help_texts = {
            'username': None,
        }


class LoginForm (forms.Form) :

    username = forms.CharField(max_length=100, )
    password = forms.CharField(widget = forms.PasswordInput)