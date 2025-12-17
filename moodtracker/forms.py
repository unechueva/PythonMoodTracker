<<<<<<< Updated upstream
=======
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Entry
from datetime import date

class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['date', 'mood', 'note']

    def clean_date(self):
        d = self.cleaned_data['date']
        if d > date.today():
            raise forms.ValidationError('Дата не может быть в будущем')
        return d
>>>>>>> Stashed changes
