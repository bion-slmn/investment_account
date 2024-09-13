from django.test import TestCase
from django.contrib.auth.models import User
from ..models import InvestmentAccount, Transaction
from decimal import Decimal


class TestInvestmentAccount(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass")

    def test_creation(self):  # sourcery skip: class-extract-method
        account = InvestmentAccount(
            name="Test Account",
            description="This is a test account",
            balance=1000.00,
            account_type=InvestmentAccount.AccountTypes.ACCOUNT_1,
            owner=self.user
        )
        account.save()
        self.assertEqual(account.name, "Test Account")
        self.assertEqual(account.description, "This is a test account")
        self.assertEqual(account.balance, 1000.00)
        self.assertEqual(account.owner, self.user)
        self.assertTrue(account.pk)

    def test_default_values(self):
        account = InvestmentAccount(owner=self.user)
        self.assertEqual(account.balance, 0.0)
        self.assertEqual(account.account_type,
                         InvestmentAccount.AccountTypes.ACCOUNT_1)

    def test_str_method(self):
        account = InvestmentAccount.objects.create(
            name="Test Account", owner=self.user)
        self.assertEqual(str(account), "Test Account")

    def test_foreign_key_relationship(self):
        account = InvestmentAccount.objects.create(
            name="Test Account", owner=self.user)
        self.assertEqual(account.owner, self.user)
        self.assertEqual(account.owner.pk, self.user.pk)

    def test_enum_choices(self):
        choices = list(InvestmentAccount.AccountTypes.choices)
        self.assertEqual(len(choices), 3)
        self.assertEqual(choices[0], ('ACC1', 'Account 1'))
        self.assertEqual(choices[1], ('ACC2', 'Account 2'))
        self.assertEqual(choices[2], ('ACC3', 'Account 3'))

    def test_create_with_all_fields(self):
        account = InvestmentAccount(
            name="Full Account",
            description="A full account with all fields",
            balance=5000.00,
            account_type=InvestmentAccount.AccountTypes.ACCOUNT_2,
            owner=self.user
        )
        account.save()
        self.assertIsNotNone(account.pk)
        self.assertEqual(account.name, "Full Account")
        self.assertEqual(account.description, "A full account with all fields")
        self.assertEqual(account.balance, 5000.00)
        self.assertEqual(account.account_type,
                         InvestmentAccount.AccountTypes.ACCOUNT_2)
        self.assertEqual(account.owner, self.user)

    def test_update_fields(self):
        account = InvestmentAccount.objects.create(
            name="Update Test",
            owner=self.user,
            balance=2000.00,
            account_type=InvestmentAccount.AccountTypes.ACCOUNT_1
        )

        account.name = "Updated Name"
        account.description = "New Description"
        account.balance = 3000.00
        account.account_type = InvestmentAccount.AccountTypes.ACCOUNT_2

        account.save()

        self.assertEqual(account.name, "Updated Name")
        self.assertEqual(account.description, "New Description")
        self.assertEqual(account.balance, 3000.00)
        self.assertEqual(account.account_type,
                         InvestmentAccount.AccountTypes.ACCOUNT_2)

    def test_delete(self):
        account = InvestmentAccount.objects.create(
            name="Delete Test",
            owner=self.user,
            balance=4000.00,
            account_type=InvestmentAccount.AccountTypes.ACCOUNT_3
        )

        account.delete()

        self.assertEqual(
            InvestmentAccount.objects.filter(
                pk=account.pk).count(), 0)


class TransactionModelTest(TestCase):
    def setUp(self):
        """
        Set up the test environment by creating users and investment accounts.
        """
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.account = InvestmentAccount.objects.create(
            name='Test Account',
            description='Test Description',
            balance=Decimal('1000.00'),
            owner=self.user
        )

    def test_create_deposit_transaction(self):
        """
        Test creating a transaction of type 'Deposit'.
        """
        transaction = Transaction.objects.create(
            transaction_by=self.user,
            transaction_type=Transaction.TransactionTypes.DEPOSIT,
            amount=Decimal('100.00'),
            account=self.account
        )
        self.assertEqual(
            transaction.transaction_type,
            Transaction.TransactionTypes.DEPOSIT)
        self.assertEqual(transaction.amount, Decimal('100.00'))
        self.assertEqual(transaction.account, self.account)
        self.assertEqual(transaction.transaction_by, self.user)

    def test_create_withdrawal_transaction(self):
        """
        Test creating a transaction of type 'Withdrawal'.
        """
        transaction = Transaction.objects.create(
            transaction_by=self.user,
            transaction_type=Transaction.TransactionTypes.WITHDRAWAL,
            amount=Decimal('50.00'),
            account=self.account
        )
        self.assertEqual(
            transaction.transaction_type,
            Transaction.TransactionTypes.WITHDRAWAL)
        self.assertEqual(transaction.amount, Decimal('50.00'))
        self.assertEqual(transaction.account, self.account)
        self.assertEqual(transaction.transaction_by, self.user)

    def test_invalid_transaction_type(self):
        """
        Test that an invalid transaction type raises a validation error.
        """
        with self.assertRaises(ValueError):
            Transaction.objects.create(
                transaction_by=self.user,
                transaction_type='InvalidType',
                amount=Decimal('50.00'),
                account='self.account'
            )

    def test_amount_decimal_field(self):
        """
        Test that the amount field correctly stores and retrieves decimal values.
        """
        transaction = Transaction.objects.create(
            transaction_by=self.user,
            transaction_type=Transaction.TransactionTypes.DEPOSIT,
            amount=Decimal('1234.56'),
            account=self.account
        )
        self.assertEqual(transaction.amount, Decimal('1234.56'))

    def test_foreign_key_relationships(self):
        """
        Test the foreign key relationships to User and InvestmentAccount.
        """
        transaction = Transaction.objects.create(
            transaction_by=self.user,
            transaction_type=Transaction.TransactionTypes.WITHDRAWAL,
            amount=Decimal('75.00'),
            account=self.account
        )
        self.assertEqual(transaction.transaction_by, self.user)
        self.assertEqual(transaction.account, self.account)
        self.assertIn(transaction, self.account.transactions.all())
        # Reverse relationship
        self.assertIn(transaction, self.user.transaction_set.all())
