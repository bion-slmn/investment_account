from django.test import TestCase
from django.contrib.auth.models import User
from ..models import InvestmentAccount

class TestInvestmentAccount(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass")

    def test_creation(self):  # sourcery skip: class-extract-method
        account = InvestmentAccount(
            name="Test Account",
            description="This is a test account",
            amount_deposited=1000.00,
            account_type=InvestmentAccount.AccountTypes.ACCOUNT_1,
            owner=self.user
        )
        account.save()
        self.assertEqual(account.name, "Test Account")
        self.assertEqual(account.description, "This is a test account")
        self.assertEqual(account.amount_deposited, 1000.00)
        self.assertEqual(account.owner, self.user)
        self.assertEqual(account.pk, not None)

    def test_default_values(self):
        account = InvestmentAccount(owner=self.user)
        self.assertEqual(account.amount_deposited, 0.0)
        self.assertEqual(account.account_type, InvestmentAccount.AccountTypes.ACCOUNT_1)

    def test_str_method(self):
        account = InvestmentAccount.objects.create(name="Test Account", owner=self.user)
        self.assertEqual(str(account), "Test Account")

    def test_foreign_key_relationship(self):
        account = InvestmentAccount.objects.create(name="Test Account", owner=self.user)
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
            amount_deposited=5000.00,
            account_type=InvestmentAccount.AccountTypes.ACCOUNT_2,
            owner=self.user
        )
        account.save()
        self.assertIsNotNone(account.pk)
        self.assertEqual(account.name, "Full Account")
        self.assertEqual(account.description, "A full account with all fields")
        self.assertEqual(account.amount_deposited, 5000.00)
        self.assertEqual(account.account_type, InvestmentAccount.AccountTypes.ACCOUNT_2)
        self.assertEqual(account.owner, self.user)

    def test_update_fields(self):
        account = InvestmentAccount.objects.create(
            name="Update Test",
            owner=self.user,
            amount_deposited=2000.00,
            account_type=InvestmentAccount.AccountTypes.ACCOUNT_1
        )
        
        account.name = "Updated Name"
        account.description = "New Description"
        account.amount_deposited = 3000.00
        account.account_type = InvestmentAccount.AccountTypes.ACCOUNT_2
        
        account.save()
        
        self.assertEqual(account.name, "Updated Name")
        self.assertEqual(account.description, "New Description")
        self.assertEqual(account.amount_deposited, 3000.00)
        self.assertEqual(account.account_type, InvestmentAccount.AccountTypes.ACCOUNT_2)

    def test_delete(self):
        account = InvestmentAccount.objects.create(
            name="Delete Test",
            owner=self.user,
            amount_deposited=4000.00,
            account_type=InvestmentAccount.AccountTypes.ACCOUNT_3
        )
        
        account.delete()
        
        self.assertEqual(InvestmentAccount.objects.filter(pk=account.pk).count(), 0)
