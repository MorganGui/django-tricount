# models.py
from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(User, related_name='membership_groups')

    def __str__(self):
        return self.name

class Expense(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses_paid')
    participants = models.ManyToManyField(User, related_name='expenses_shared')

    def __str__(self):
        return self.description
