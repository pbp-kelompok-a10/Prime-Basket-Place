from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from account.models import Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['nickname', 'age', 'profile_picture']
        widgets = {
            'nickname': forms.TextInput(attrs={
                'placeholder': 'Your Name...',
                'class': 'w-full rounded-md border border-gray-300 bg-gray-100 p-2 focus:outline-none focus:ring-2 focus:ring-[#391C8C]'
            }),
            'age': forms.NumberInput(attrs={
                'placeholder': 'Your Age...',
                'class': 'w-full rounded-md border border-gray-300 bg-gray-100 p-2 focus:outline-none focus:ring-2 focus:ring-[#391C8C]'
            }),
            'profile_picture': forms.URLInput(attrs={
                'placeholder': 'https://example.com/profile.jpg',
                'class': 'w-full rounded-md border border-gray-300 bg-gray-100 p-2 focus:outline-none focus:ring-2 focus:ring-[#391C8C]'
            }),
        }

