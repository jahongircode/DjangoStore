from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms


class SearchForm(forms.Form):
    search_product = forms.CharField(max_length=880)

class RegisterForm(UserCreationForm):
    email = forms.EmailField

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']