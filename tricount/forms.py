# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Group, Expense

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']

class AddMemberForm(forms.Form):
    username = forms.CharField(max_length=150)

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount', 'date', 'payer', 'participants']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
