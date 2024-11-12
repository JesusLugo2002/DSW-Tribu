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
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save(self):
        wave = super().save(commit=False)
        wave.user = self.user
        wave.echo = self.echo
        wave = super().save()
        return wave


class EditWaveForm(forms.ModelForm):
    class Meta:
        model = Wave
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
