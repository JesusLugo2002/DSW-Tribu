from django import forms

from .models import Echo


class AddEchoForm(forms.ModelForm):
    class Meta:
        model = Echo
        fields = ['content']


class EditEchoForm(forms.ModelForm):
    class Meta:
        model = Echo
        fields = ['content']
