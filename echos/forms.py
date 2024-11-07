from django import forms

from .models import Echo
from waves.models import Wave


class AddEchoForm(forms.ModelForm):
    class Meta:
        model = Echo
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class EditEchoForm(forms.ModelForm):
    class Meta:
        model = Echo
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class AddWaveForm(forms.ModelForm):
    class Meta:
        model = Wave
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
