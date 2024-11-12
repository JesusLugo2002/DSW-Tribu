from django import forms
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):
    username = forms.SlugField(max_length=64, required=True)
    password = forms.CharField(max_length=64, required=True, widget=forms.PasswordInput)

class SignupForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = dict(password=forms.PasswordInput)
        help_texts = dict(username=None)
