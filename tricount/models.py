from django.contrib.auth.models import User
from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(User, related_name='member_of_groups')  # Modifier ici
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Expense(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='expenses')
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses_paid')
    split_between = models.ManyToManyField(User, related_name='expenses_shared')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.description} - {self.amount}'

class Settlement(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='settlements')
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='settlements_paid')
    paid_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='settlements_received')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.paid_by} owes {self.paid_to} {self.amount}'
