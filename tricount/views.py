# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import Group, Expense
from .forms import GroupForm, ExpenseForm, SignUpForm

def home(request):
    groups = Group.objects.all()
    return render(request, 'tricount/home.html', {'groups': groups})

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.save()
            group.members.add(request.user)
            return redirect('group_detail', group_id=group.id)
    else:
        form = GroupForm()
    return render(request, 'tricount/create_group.html', {'form': form})

@login_required
def group_detail(request, group_id):
    group = Group.objects.get(id=group_id)
    return render(request, 'tricount/group_detail.html', {'group': group})

@login_required
def add_expense(request, group_id):
    group = Group.objects.get(id=group_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.group = group
            expense.save()
            form.save_m2m()
            return redirect('group_detail', group_id=group.id)
    else:
        form = ExpenseForm()
    return render(request, 'tricount/add_expense.html', {'form': form, 'group': group})

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
