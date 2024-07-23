from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Group, Expense, Settlement
from .forms import GroupForm, ExpenseForm

def home(request):
    return render(request, 'tricount/home.html')

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user
            group.save()
            form.save_m2m()
            return redirect('group_detail', group_id=group.id)
    else:
        form = GroupForm()
    return render(request, 'tricount/create_group.html', {'form': form})

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'tricount/group_detail.html', {'group': group})

@login_required
def add_expense(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.group = group
            expense.paid_by = request.user
            expense.save()
            form.save_m2m()
            return redirect('group_detail', group_id=group.id)
    else:
        form = ExpenseForm()
    return render(request, 'tricount/add_expense.html', {'form': form, 'group': group})
