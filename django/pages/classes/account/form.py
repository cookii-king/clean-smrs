from django import forms
from ...models import Account
from pages.validators import *

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'password', 'name', 'username']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        CustomEmailValidator().validate(email)
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        CustomPasswordValidator().validate(password)
        return password
