
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='Nome',
        help_text='Inserisci il nome',
        error_messages={
            'required':'Il nome è obbligatorio',
            'max_length':'Il nome non può superare 30 caratteri'
        }
    )
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "is_active")
