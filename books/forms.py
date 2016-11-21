from django.contrib.auth.forms import AuthenticationForm 
from django import forms

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password", max_length=30, widget=forms.PasswordInput)

class ChangePasswordForm(forms.Form):
    #widget.passwordInput
    password_1 = forms.CharField(label="New password", max_length=30)
    password_2 = forms.CharField(label="Verify password", max_length=30)

    
