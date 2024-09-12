from django.contrib.auth.models import User
from django.db import models


class InvestmentAccount(models.Model):
    """
InvestmentAccount represents a user's investment account in the system,
including various account types.
It stores information about the account's name, description, amount deposited,
 account type, and the account owner.

AccountTypes:
    ACCOUNT_1: Represents the first type of investment account.
    ACCOUNT_2: Represents the second type of investment account.
    ACCOUNT_3: Represents the third type of investment account.
"""

    class AccountTypes(models.TextChoices):
        ACCOUNT_1 = 'ACC1', 'Account 1'
        ACCOUNT_2 = 'ACC2', 'Account 2'
        ACCOUNT_3 = 'ACC3', 'Account 3'

    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    balance = models.DecimalField(
        'Deposit is + and withdraw -',
        max_digits=10,
        decimal_places=2,
        default=0.0)
    account_type = models.CharField(
        max_length=5,
        choices=AccountTypes.choices,
        default=AccountTypes.ACCOUNT_1)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')

    def __str__(self):
        return self.name


class Transaction(models.Model):
    class TransactionTypes(models.TextChoices):
        DEPOSIT = 'Deposit'
        WITHDRAWAL = 'Withdrawal'

    transaction_type = models.CharField(
        max_length=15, choices=TransactionTypes.choices)
    created_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(
        'Deposit is + and withdraw -',
        max_digits=10,
        decimal_places=2)
    transaction_by = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(
        InvestmentAccount,
        on_delete=models.CASCADE,
        related_name='transactions')
