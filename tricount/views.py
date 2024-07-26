import functools
from gc import get_objects
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import Group, Expense, Profile, ParticipantPayment
from .forms import GroupForm, ExpenseForm, ReceiptForm, SignUpForm, AddMemberForm, CustomExpenseForm
from .utils import get_exchange_rates

def calculate_amount(entity):
    return (functools.reduce(lambda a, b: a + b.amount, entity, 0) or 0)

def calculate_available_amount(expenses, receipts):
    return calculate_amount(receipts) - calculate_amount(expenses)

def calculate_average(entity, members):
    return (functools.reduce(lambda a, b: a + b.amount, entity, 0) / len(members)) or 0

def home(request):
    if request.user.is_authenticated:
        groups = request.user.membership_groups.all()
        groups = map(lambda x: {"id": x.id, "name": x.name, "amount": calculate_available_amount(x.expenses.all(), x.receipts.all())}, groups)
        return render(request, 'tricount/home.html', {'groups': groups})
    else:
        return redirect('login')

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            group.members.add(request.user)
            return redirect('group_detail', group_id=group.id)
    else:
        form = GroupForm()
    return render(request, 'tricount/create_group.html', {'form': form})

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    expenses = group.expenses.all()
    total_expenses_amount = functools.reduce(lambda a, b: a + b.amount, expenses, 0)
    receipts = group.receipts.all()
    total_receipts_amount = functools.reduce(lambda a, b: a + b.amount, receipts, 0)

    members = group.members.all()
    average_expenses = calculate_average(expenses, members)
    average_receipts = calculate_average(receipts, members)
    solde = calculate_available_amount(group.expenses.all(), group.receipts.all())
    max_receipt = 0

    for member in members:
        member.group_receipts_amount = calculate_amount(member.receipts_payer.filter(group=group))
        if member.group_receipts_amount > max_receipt:
            max_receipt = member.group_receipts_amount
    
    for member in members:
        member.group_balance = round(max_receipt - member.group_receipts_amount)

    return render(request, 'tricount/group_detail.html', {
        'group': group,
        'members': members,
        "solde": solde,
        'expenses': expenses,
        'total_expenses_amount': total_expenses_amount,
        'receipts': receipts,
        'total_receipts_amount': total_receipts_amount,
        "average_expenses": round(average_expenses),
        "average_receipts": round(average_receipts)
    })

@login_required
def add_member(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()
            if user:
                group.members.add(user)
                return redirect('group_detail', group_id=group.id)
            else:
                return render(request, 'tricount/add_member.html', {'form': form, 'group': group, 'error': f"""L'utilisateur {username} n'existe pas !"""})
    else:
        form = AddMemberForm()
    return render(request, 'tricount/add_member.html', {'form': form, 'group': group})

@login_required
def edit_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('group_detail', group_id=group.id)
    else:
        form = GroupForm(instance=group)
    return render(request, 'tricount/edit_group.html', {'form': form, 'group': group})

@login_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        group.delete()
        return redirect('home')
    return render(request, 'tricount/delete_group.html', {'group': group})

@login_required
def add_expense(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.group = group
            expense.save()
            form.save_m2m()
            group.save()
            return redirect('group_detail', group_id=group.id)
    else:
        form = ExpenseForm()
        form.fields["payer"].queryset = group.members.all()
        form.fields["participants"].queryset = group.members.all()
    return render(request, 'tricount/add_expense.html', {'form': form, 'group': group})

@login_required
def add_receipt(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = ReceiptForm(request.POST)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.group = group
            receipt.save()
            form.save_m2m()
            group.save()
            return redirect('group_detail', group_id=group.id)
    else:
        form = ReceiptForm()
        form.fields["payer"].queryset = group.members.all()
    return render(request, 'tricount/add_receipt.html', {'form': form, 'group': group})

@login_required
def add_custom_expense(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = CustomExpenseForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            payments = form.cleaned_data['payments']
            expense = Expense.objects.create(
                group=group,
                description=description,
                payer=request.user
            )
            for payment_data in payments:
                member = payment_data['member']
                amount_paid = payment_data['amount_paid']
                ParticipantPayment.objects.create(
                    expense=expense,
                    group=group,
                    member=member,
                    amount_paid=amount_paid
                )
            group.save()
            return redirect('group_detail', group_id=group.id)
    else:
        form = CustomExpenseForm()
    return render(request, 'tricount/add_custom_expense.html', {'form': form, 'group': group})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def exchange_rate_view(request):
    api_key = '7774bcaf1def23886ebd144d9c1939a8'
    rates = get_exchange_rates(api_key)
    if rates:
        return render(request, 'tricount/exchange_rates.html', {'rates': rates})
    else:
        return render(request, 'tricount/exchange_rates.html', {'error': 'Unable to fetch exchange rates'})
