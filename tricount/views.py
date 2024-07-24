# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import Group, Expense
from .forms import GroupForm, ExpenseForm, SignUpForm, AddMemberForm

def home(request):
    groups = Group.objects.all()
    return render(request, 'tricount/home.html', {'groups': groups})

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
    return render(request, 'tricount/group_detail.html', {'group': group})

@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.members.add(request.user)
    return redirect('group_detail', group_id=group.id)

@login_required
def add_member(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = get_object_or_404(User, username=username)
            group.members.add(user)
            return redirect('group_detail', group_id=group.id)
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
