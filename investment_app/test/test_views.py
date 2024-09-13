from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import InvestmentAccount, Transaction
from unittest.mock import patch, MagicMock


class UserViewTest(TestCase):
    def setUp(self):
        """
        Set up the test environment by initializing the APIClient.
        """
        self.client = APIClient()
        self.url = reverse('register-user')  

    def test_create_user_success(self):
        """
        Test the successful creation of a user with valid data.
        """
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@example.com',
            'full_name': 'Test User'
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'testuser@example.com')
        self.assertNotIn('password', response.data)

    def test_create_user_failure(self):
        """
        Test the failure case when invalid data is provided.
        """
        data = {
            'username': '',  # Invalid username
            'password': 'short',  # Invalid password
            'email': 'not-an-email',
            'full_name': 'Test User'
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)

    def test_handle_exceptions(self):
        """
        Test that exceptions are properly handled and return a 400 status.
        """
        # Mock the serializer to raise an exception
        response = self.client.post(self.url, {}, format='json')

        # Ensure the response status is 400 and contains the error message
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class AccountViewTest(TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        self.client = APIClient()
        
        # Create users with different roles
      
        self.user = User.objects.create_user(username='user', password='userpassword')
    
        # Create investment accounts with different types
        self.account_1 = InvestmentAccount.objects.create(name='Account 1', account_type='ACC1', owner=self.user)
        self.account_2 = InvestmentAccount.objects.create(name='Account 2.0', account_type='ACC2', owner=self.user)
        self.account_3 = InvestmentAccount.objects.create(name='Account 3', account_type='ACC3', owner=self.user)
        
        # Create a transaction for account type 2
        Transaction.objects.create(
            transaction_by=self.user,
            transaction_type='Deposit',
            amount=200.00,
            account=self.account_2
        )
        response = self.client.post(reverse('login'),  {'username':'user', 'password':'userpassword'}, format='json')
        self.token = response.data

    def test_view_account_type_1(self):
        """
        Test that a user with permissions to view Account Type 1 can do so.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        url = reverse('view-account', args=[self.account_1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['account']['id'], self.account_1.id)
        self.assertEqual(response.data['transcations'], [])

    def test_view_account_type_2(self):
        """
        Test that a user with full permissions for Account Type 2 can view the account and transactions.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        url = reverse('view-account', args=[self.account_2.id])
        response = self.client.get(url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['account']['id'], self.account_2.id)
        self.assertEqual(len(response.data['transcations']), 1)

    def test_view_account_type_3(self):
        """
        Test that a user without permission to view Account Type 3 receives a permission denied error.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        url = reverse('view-account', args=[self.account_3.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Permission Denied, You do not have permission to perform this action.')

    def test_unauthenticated_access(self):
        """
        Test that unauthenticated access to the view returns a 401 unauthorized error.
        """
        url = reverse('view-account', args=[self.account_1.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('investment_app.views.get_transactions')
    @patch('investment_app.views.AccountView._check_account_permission')
    def test_successful_permission_check(self, mock_check_permission, mock_get_transactions):
        # Mock _check_account_permission to return the account
        mock_check_permission.return_value = self.account_3
        mock_get_transactions.return_value = []
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        url = reverse('view-account', args=[self.account_3.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('account', response.data)
        
        mock_check_permission.assert_called_once()



class CreateAnAccountTest(TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        self.client = APIClient()
        
        self.user = User.objects.create_user(username='user', password='password')
        
        response = self.client.post(reverse('login'),  {'username':'user', 'password':'password'}, format='json')
        self.token = response.data     
        # Create some test data

        self.account_1 = {
            'name': 'Account 1.0',
            'account_type': 'ACC1',
            'balance': 200
        }
        self.account_data_with_balance = {
            'name': 'Account 2.0',
            'account_type': 'ACC2',
            'balance': 200
        }
        self.account_data_without_balance = {
            'name': 'Account 3',
            'account_type': 'ACC3'
        }
    def creation__and_account_type_1(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        url = reverse('create-account')
        response = self.client.post(url, self.account_1, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Transaction.objects.all().count(), 1)

    def test_create_account_with_balance__and_account_type_2(self):
        """
        Test account creation with a positive balance.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        url = reverse('create-account')
        response = self.client.post(url, self.account_data_with_balance, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Account 2.0')
        self.assertEqual(response.data['balance'], '200.00')
        self.assertEqual(Transaction.objects.all().count(), 1)

    def test_create_account_without_balance_and_account_type_3(self):
        """
        Test account creation without a balance.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        url = reverse('create-account')
        response = self.client.post(url, self.account_data_without_balance, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Account 3')
        self.assertEqual(response.data['balance'], '0.00')
        # balance is 0 so no tranction is created
        self.assertEqual(Transaction.objects.all().count(), 0) 

    def test_create_account_without_permission(self):
        """
        Test that a user without permission cannot create an account.
        """
        url = reverse('create-account')
        response = self.client.post(url, self.account_data_with_balance, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AccountUpdateViewTest(TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        self.client = APIClient()
      
        self.user = User.objects.create_user(username='user', password='password')
  
        response = self.client.post(reverse('login'),  {'username':'user', 'password':'password'}, format='json')
        self.token = response.data
        # Create some test data
        self.account_1 = InvestmentAccount.objects.create(name='Account 1', account_type='ACC1', owner=self.user)
        self.account_2 = InvestmentAccount.objects.create(name='Account 2.0', account_type='ACC2', owner=self.user)
        self.account_2_1 = InvestmentAccount.objects.create(name='Account 2.0', account_type='ACC2', owner=self.user, balance=1000)
        self.account_3 = InvestmentAccount.objects.create(name='Account 3', account_type='ACC3', owner=self.user)
        
    def test_deposit_account_success(self):
        """
        Test that a user with permission can successfully update an account.
        """
        url = reverse('update-account', args=[self.account_2.id])
        data = {'balance': 1000}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], '1000.00')
        trans = Transaction.objects.all()
        self.assertEqual(trans.count(), 1)
        self.assertEqual(trans[0].transaction_type, 'Deposit')

    def test_withdraw_success(self):
        """
        Test that a user with permission can successfully update an account.
        """
        url = reverse('update-account', args=[self.account_2_1.id])
        data = {'balance': -200}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], '800.00')
        trans = Transaction.objects.all()
        self.assertEqual(trans.count(), 1)
        self.assertEqual(trans[0].transaction_type, 'Withdrawal')

    def test_withdraw_fail(self):
        """
        Test that a user with permission can successfully update an account.
        """
        url = reverse('update-account', args=[self.account_2.id])
        data = {'balance': -200}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        trans = Transaction.objects.all()
        self.assertEqual(trans.count(), 0)
       
        
    def test_update_account_permission_denied(self):
        """
        Test that a user without permission cannot update an account they do not own.
        """
        url = reverse('update-account', args=[self.account_1.id])
        data = {'balance': 1000}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error'], 'Permission Denied, You do not have permission to perform this action.')

    def test_update_account_permission_denied(self):
        """
        Test that a user without permission cannot update an account they do not own.
        """
        url = reverse('update-account', args=[self.account_3.id])
        data = {'balance': 1000}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error'], 'Permission Denied, You do not have permission to perform this action.')
        
    def test_update_account_invalid_data(self):
        """
        Test that invalid data results in a validation error.
        """
        url = reverse('update-account', args=[self.account_2.id])
        data = {'balance': 'value'}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
      
class DeleteAccount(TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        self.client = APIClient()
      
        self.user = User.objects.create_user(username='user', password='password')
  
        response = self.client.post(reverse('login'),  {'username':'user', 'password':'password'}, format='json')
        self.token = response.data
        # Create some test data
        self.account_1 = InvestmentAccount.objects.create(name='Account 1', account_type='ACC1', owner=self.user)
        self.account_2 = InvestmentAccount.objects.create(name='Account 2.0', account_type='ACC2', owner=self.user)
        self.account_3 = InvestmentAccount.objects.create(name='Account 3', account_type='ACC3', owner=self.user)
    
    def test_delete_account_1(self):
        url = reverse('delete-account', args=[self.account_1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_account_2(self):
        url = reverse('delete-account', args=[self.account_2.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_account_3(self):
        url = reverse('delete-account', args=[self.account_3.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_unkouwn_account_1(self):
        url = reverse('delete-account', args=[41])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
      