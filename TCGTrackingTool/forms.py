from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Card


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['product_ID', 'card_name',
                  'image_url', 'category_ID', 'group_ID']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2' ]