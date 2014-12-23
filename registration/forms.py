from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import re

class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=32)
    lastname = forms.CharField(max_length=32)
    email = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32)
    confirmation = forms.CharField(max_length=32)

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        if not re.match(r'([A-Z]|[0-9])', cleaned_data['password']) or len(cleaned_data['password']) < 8:
            raise ValidationError('This password is not enough safe. It must contains numbers and uppercase letters.')

        if cleaned_data['password'] != cleaned_data['confirmation']:
            raise ValidationError('Password doesnt match with confirmation')

        return cleaned_data
        
    def clean_email(self):

        if not re.match(r'\w+@\w+\.\w+', self.cleaned_data['email']):
            raise ValidationError('This is no a valid email')

        try:
            User.objects.get(email=self.cleaned_data['email'])
            raise ValidationError('Already exist a user with this email')
        except User.DoesNotExist:
            return self.cleaned_data['email']
