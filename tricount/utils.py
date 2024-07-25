# utils.py
import requests
from .models import Expense, MemberBalance

def get_exchange_rates(api_key):
    url = f"https://api.exchangerate-api.com/v4/latest/USD?apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['rates']
    else:
        return None

def calculate_balances(group):
    members = group.members.all()
    MemberBalance.objects.filter(group=group).delete()

    for member in members:
        balance, created = MemberBalance.objects.get_or_create(group=group, member=member)
        balance.balance = 0
        balance.save()

    expenses = Expense.objects.filter(group=group)
    for expense in expenses:
        total_participants = expense.participants.count()
        share = expense.amount / total_participants
        payer_balance, created = MemberBalance.objects.get_or_create(group=group, member=expense.payer)
        payer_balance.balance += expense.amount
        payer_balance.save()

        for participant in expense.participants.all():
            participant_balance, created = MemberBalance.objects.get_or_create(group=group, member=participant)
            participant_balance.balance -= share
            participant_balance.save()
