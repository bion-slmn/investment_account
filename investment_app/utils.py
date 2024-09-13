from .models import InvestmentAccount, Transaction
from django.shortcuts import get_object_or_404
from .serializer import TransactionSeializer
from django.http import HttpRequest
from typing import List, Optional
from .signals import account_changed
from django.core.cache import cache


def get_transactions(
        account: InvestmentAccount,
        limit: Optional[int] = None) -> List:
    """Retrieve transactions for a specified investment account.

    Args:
        account (InvestmentAccount): The investment account for
          which to retrieve transactions.
        limit (int, optional): The maximum number of 
            transactions to return. Defaults to None.

    Returns:
        TransactionSerializer or None: A serialized representation
          of the transactions if found,
        otherwise None if no transactions exist.
    """

    transactions = account.transactions.all().order_by('-created_at')
    if limit:
        transactions = transactions[:limit]

    return TransactionSeializer(transactions,
                                many=True).data if transactions else None


def create_transaction(
        request: HttpRequest,
        instance: InvestmentAccount) -> None:
    """Create a transaction for the specified investment account.

    Args:
        request (HttpRequest): The HTTP request containing transaction data.
        instance (InvestmentAccount): The investment account instance to 
        which the transaction applies.

    Returns:
        None: This function does not return a value.
    """
    amount = request.data.get('balance', 0)
    if amount != 0:
        account_changed.send(
            sender=InvestmentAccount,
            amount=amount,
            user=request.user,
            instance=instance
        )


def delete_caches(cache_keys: list) -> None:
    """
    Deletes multiple cache entries in a single operation.

    Args:
        cache_keys (list): A list of cache key strings to delete.

    Example:
        delete_caches([f'account_id_{account_id}', f'user_id_{instance.owner}'])
    """
    cache.delete_many(cache_keys)
