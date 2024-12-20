from django import forms

from .models import Echo


class AddEchoForm(forms.ModelForm):
    class Meta:
        model = Echo
        fields = ['content']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
    
    def save(self) -> Echo:
        echo = super().save(commit=False)
        echo.user = self.user
        echo = super().save()
        return echo


class EditEchoForm(forms.ModelForm):
    class Meta:
        model = Echo
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
