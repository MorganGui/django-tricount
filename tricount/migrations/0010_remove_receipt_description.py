# Generated by Django 5.0.7 on 2024-07-26 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tricount', '0009_alter_expense_date_alter_expense_group_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receipt',
            name='description',
        ),
    ]
