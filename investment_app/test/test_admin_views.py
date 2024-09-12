from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from ..models import Transaction, InvestmentAccount

User = get_user_model()

class AdminViewTest(APITestCase):

    def setUp(self):
        """Set up test data, including users, accounts, and transactions."""
        self.client = APIClient()

        # Create admin user and regular user
        self.admin_user = User.objects.create_superuser(username='admin', password='password')
        self.regular_user = User.objects.create_user(username='user', password='password')

        # Create an investment account for the user
        self.account = InvestmentAccount.objects.create(
            name="Account 1", account_type="ACC1", owner=self.regular_user, balance=1000)

        # Create a transaction for the account
        self.transaction = Transaction.objects.create(
            account=self.account, transaction_type='deposit', amount=500, transaction_by=self.regular_user)

        # Authentication tokens
        self.client.force_authenticate(user=self.admin_user)

    def test_get_user_transactions_success(self):
        """Test that an admin user can retrieve a user's transactions."""
        url = reverse('view-user-accounts', args=[self.regular_user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Username', response.data)
        self.assertIn('transactions', response.data)
        
        self.assertEqual(response.data['Username'], self.regular_user.username)
        self.assertEqual(response.data['total_balance'], 1000)  # Check total balance is correct
        self.assertEqual(len(response.data['transactions']), 1)  # Check the number of transactions

    def test_get_user_transactions_with_date_range(self):
        """Test filtering user transactions within a valid date range."""
        url = reverse('view-user-accounts', args=[self.regular_user.id])
        response = self.client.get(url, {'end_date': '2024-07-31'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['To'], '2024-07-31')
        self.assertIn('transactions', response.data)
        self.assertEqual(len(response.data['transactions']), 1)

    def test_get_user_transactions_invalid_date(self):
        """Test that an invalid date range raises a validation error."""
        url = reverse('view-user-accounts', args=[self.regular_user.id])
        response = self.client.get(url, {'start_date': 'invalid-date', 'end_date': '2024-12-31'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
     

    def test_user_without_transactions(self):
        """Test that a user with no transactions returns an empty transactions list."""
        # Create a user without any transactions
        new_user = User.objects.create_user(username='user_no_transactions', password='password')
        url = reverse('view-user-accounts', args=[new_user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('transactions', response.data)
        self.assertEqual(len(response.data['transactions']), 0)  # Expect no transactions

    def test_non_admin_access_denied(self):
        """Test that non-admin users cannot access the endpoint."""
        # Authenticate as a regular user
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('view-user-accounts', args=[self.regular_user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
