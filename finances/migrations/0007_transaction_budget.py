# Generated by Django 4.2.4 on 2023-10-07 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0006_remove_transaction_budget'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='budget',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='finances.budget'),
        ),
    ]