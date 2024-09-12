from django.dispatch import receiver, Signal
from .models import Transaction, InvestmentAccount
from django.db.models.signals import pre_save


account_changed = Signal(["amount", "user", "instance"])


@receiver(account_changed)
def create_transaction(sender, amount, user, instance, **kwargs):
    """
    Creates a new transaction whenever the account balance changes.
    The amount indicates the change, and the user is the one making the change.
    """
    transaction_type = 'Withdrawal' if amount < 0 else 'Deposit'

    Transaction.objects.create(
        transaction_type=transaction_type,
        amount=amount,
        transaction_by=user,
        account=instance
    )
