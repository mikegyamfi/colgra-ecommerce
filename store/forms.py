from django.contrib.auth.forms import UserCreationForm
from django import forms

from store.models import CustomUser

class CustomUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2 reg-form'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2 reg-form'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2 reg-form'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2 reg-form'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-2 reg-form'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-2 reg-form'}))
    phone_number = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control my-2 reg-form'}))
    class Meta():
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'phone_number']