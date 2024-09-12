# Generated by Django 4.2.10 on 2024-09-11 16:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('investment_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='investmentaccount',
            old_name='amount_deposited',
            new_name='balance',
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('DEP', 'Deposit'), ('WDR', 'Withdrawal')], max_length=3)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Deposit is + and withdraw -')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='investment_app.investmentaccount')),
                ('transaction_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
