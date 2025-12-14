from django import forms
from .models import Entry
from datetime import date

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['date', 'mood', 'note']

    def clean_date(self):
        d = self.cleaned_data['date']
        if d > date.today():
            raise forms.ValidationError('Дата не может быть в будущем')
        return d
