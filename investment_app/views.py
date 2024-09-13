from .models import InvestmentAccount, Transaction
from django.db.models import Prefetch
from rest_framework.views import APIView
from .permissions import AccountTypePermission
from .decorator import handle_exceptions
from rest_framework.response import Response
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from .serializer import InvestmentAccountSerializer, UserSerializer, DateSerialializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status
from django.core.exceptions import PermissionDenied
from .utils import get_transactions, create_transaction, delete_caches
from django.http import Http404
from django.contrib.auth.models import User
from datetime import date
from typing import Dict
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache




class UserView(APIView):
    permission_classes = [AllowAny]

    @handle_exceptions
    def post(self, request: HttpRequest) -> Response:
        """
        Creates a new user based on the provided data.
        Args:
            request (HttpRequest): The HTTP request object containing the data.

        Returns:
            Response: A response object containing the created user data
              if successful, or error messages if validation fails.

        Raises:
            ValidationError: If the provided data is invalid.
        """

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountView(APIView):
    permission_classes = [AccountTypePermission, IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @handle_exceptions
    def get(self, request: HttpRequest, account_id: str) -> Response:
        """
        Handles GET requests for retrieving an investment account by its ID.
        Args:
            request (HttpRequest): The HTTP request object containing the request data.
            account_id (int): The ID of the investment account to retrieve.

        Returns:
            Response: A Response object containing the serialized account data.
        """
        cache_key = f'account_id_{account_id}'
        account = self._check_account_permission(request, account_id)
        
        if cached_data := cache.get(cache_key):
            results = cached_data
        else:
            transactions = get_transactions(account)
            results = {
                'account': InvestmentAccountSerializer(account).data,
                'transcations': transactions or []
            }
            cache.set(cache_key, results, timeout=5*60*60)
        return Response(results)

    @handle_exceptions
    def post(self, request: HttpRequest) -> Response:
        """
        Creates a new investment account based on the provided data.

        Args:
            request (HttpRequest): The HTTP request object containing the data for the new account.

        Returns:
            Response: A response object containing the created account data
              if successful, or error messages if validation fails.

        Raises:
            ValidationError: If the provided data is invalid.
        """

        serializer = InvestmentAccountSerializer(
            data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        instance = serializer.save(owner=request.user)
        create_transaction(request, instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @handle_exceptions
    def put(self, request: HttpRequest, account_id: str) -> Response:
        """
        Updates a specified account with new data after verifying permissions.
        Args:
            request (HttpRequest): The HTTP request object containing the new data
            account_id (str): The unique identifier of the account to be updated.

        Returns:
            Response: A response object containing the updated account data
              if successful, or error messages if validation fails.

        Raises:
            PermissionError: If the user does not have permission to update the account.
            NotFoundError: If the account with the specified ID does not exist.
        """

        account = self._check_account_permission(request, account_id)
        serializer = InvestmentAccountSerializer(
            account, data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            create_transaction(request, instance)
            delete_caches([f'account_id_{account_id}', f'user_id_{instance.owner}'])
            return Response(serializer.data, 200)
        return Response(serializer.errors, 400)

    @handle_exceptions
    def delete(self, request: HttpRequest, account_id: str) -> Response:
        """
        Deletes a specified account after verifying permissions.

        Args:
            request (HttpRequest): The HTTP request object containing the request data.
            account_id (str): The unique identifier of the account to be deleted.

        Returns:
            Response: A response object indicating the result of the deletion operation.

        Raises:
            PermissionError: If the user does not have permission to delete the account.
            NotFoundError: If the account with the specified ID does not exist.
        """

        account = self._check_account_permission(request, account_id)
        account.delete()
        return Response('Sucessfully deleted')

    def _check_account_permission(
            self,
            request: HttpRequest,
            account_id: str) -> InvestmentAccount:
        """
        Checks if the user has permission to access a specific investment account.

        Args:
            request (HttpRequest): The HTTP request object containing the request data.
            account_id (str): The ID of the investment account to check permissions for.

        Returns:
            InvestmentAccount: The investment account object if permissions are granted.

        Raises:
            Http404: If the investment account does not exist or the user lacks permissions.
        """
        try:
            user = request.user
            account = get_object_or_404(
                InvestmentAccount.objects.prefetch_related('transactions'),
                id=account_id)
            self.check_object_permissions(request, account)
            return account
        except Http404 as error:
            raise Http404(error)
        except Exception as error:
            raise PermissionDenied(error) from error


class AdminView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]

    @handle_exceptions
    def get(self, request: HttpRequest, user_id: str) -> Response:
        """Handle GET requests to retrieve user transaction data within a date range.

        Args:
            request (HttpRequest): The HTTP request containing query parameters for date filtering.
            user_id (str): The ID of the user whose transactions are to be retrieved.

        Returns:
            Response: A response object containing the user's transaction data and status code 200.
        """
        today = date.today()
        start_date = request.query_params.get('start_date') or today
        end_date = request.query_params.get('end_date')
        
        cache_key = f'user_id_{user_id}'
        cache_data = cache.get(cache_key)
        
        if not end_date and cache_data:
            results = cache_data
            
        else:
            user = self.get_filtered_user(user_id, start_date, end_date)     
            results = self.get_user_transactions(user, start_date, end_date)

            
        return Response(results, 200)
    
    def get_user_transactions(self, user: User, start_date: date, end_date: date = None) -> Dict[str, str]:
        """Retrieve a summary of a user's transactions and total balance.

        Args:
            user (User): The user for whom to retrieve transaction data.

        Returns:
            dict: A dictionary containing the username, total balance, and a list of transactions.
        """

        results = {
            'Username': user.username,
            'total_balance' : 0,
            'transactions' : [],
            'From' :start_date,
            'To' :end_date or "All Transactions"
        }
        for account in user.accounts.all():
            results['total_balance'] += account.balance
            transactions = account.transactions.values()
            for transaction in transactions:
                transaction['account_type'] = account.account_type
            results['transactions'].extend(transactions)

        if not end_date:
            cache_key = f'user_id_{user.id}'
            cache.set(cache_key, results, timeout=2*60*60)

        return results
    
    def get_filtered_user(self, user_id: str, start_date: date, end_date: date = None) -> User:
        """Retrieve a user and their associated transactions within a specified date range.

        Args:
            user_id (str): The ID of the user to retrieve.
            start_date (date): The start date for filtering transactions usually today.
            end_date (date, optional): The end date for filtering transactions. Defaults to None
                    enddate is a date in the past.

        Returns:
            User: The user instance with preloaded transactions.

        Raises:
            ValueError: If start_date or end_date is not a date object.
        """

        if end_date is None:
            transactions = Transaction.objects.all()
        else:
            serializer = DateSerialializer(data={'start_date': start_date, 'end_date': end_date})
            serializer.is_valid(raise_exception=True)

            transactions = Transaction.objects.filter(
                created_at__lte=f'{start_date} 23:59:59',
                created_at__gte=f'{end_date} 23:59:59',
                )
                    
        queryset = User.objects.prefetch_related(
            Prefetch('accounts__transactions', queryset=transactions))
        return get_object_or_404(queryset, id=user_id)

