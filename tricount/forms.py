from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Group, Expense, Profile, ParticipantPayment, Receipt

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

class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ['amount', 'date', 'payer']

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['currency']

class CustomExpenseForm(forms.Form):
    description = forms.CharField(max_length=255)
    payments = forms.CharField(widget=forms.Textarea)

    def clean_payments(self):
        payments_str = self.cleaned_data['payments']
        payments_list = payments_str.splitlines()
        payments = []
        for payment_str in payments_list:
            try:
                username, amount_paid = payment_str.split(',')
                user = User.objects.get(username=username.strip())
                payments.append({'member': user, 'amount_paid': float(amount_paid.strip())})
            except ValueError:
                raise forms.ValidationError("Format invalide pour les paiements.")
            except User.DoesNotExist:
                raise forms.ValidationError(f"Utilisateur {username.strip()} n'existe pas.")
        return payments
