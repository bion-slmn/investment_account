# Generated by Django 4.2.10 on 2024-09-12 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('investment_app', '0002_rename_amount_deposited_investmentaccount_balance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investmentaccount',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Deposit is + and withdraw -'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='investment_app.investmentaccount'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('Deposit', 'Deposit'), ('Withdrawal', 'Withdrawal')], max_length=15),
        ),
    ]
