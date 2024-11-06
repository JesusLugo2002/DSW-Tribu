from django import forms

from .models import Echo


class AddEchoForm(forms.ModelForm):
    class Meta:
        model = Echo
        fields = ['content']
