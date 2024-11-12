from django import forms

from .models import Wave


class AddWaveForm(forms.ModelForm):
    class Meta:
        model = Wave
        fields = ['content']

    def __init__(self, user, echo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.echo = echo

    def save(self) -> Wave:
        wave = super().save(commit=False)
        wave.user = self.user
        wave.echo = self.echo
        wave = super().save()
        return wave


class EditWaveForm(forms.ModelForm):
    class Meta:
        model = Wave
        fields = ['content']
