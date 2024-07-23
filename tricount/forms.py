from django import forms
from .models import Group, Expense

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'members']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount', 'split_between']
