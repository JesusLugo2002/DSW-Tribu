from django import forms
from .models import Wave

class EditWaveForm(forms.ModelForm):
    class Meta:
        model = Wave
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'