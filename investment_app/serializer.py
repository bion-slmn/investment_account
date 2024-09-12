from rest_framework import serializers
from .models import InvestmentAccount, Transaction
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password



class InvestmentAccountSerializer(serializers.ModelSerializer):
    account_type = serializers.ChoiceField(choices=InvestmentAccount.AccountTypes.choices)

    class Meta:
        model = InvestmentAccount
        fields = '__all__'

    def create(self, validated_data):
        """Create a new investment account with validated data.

        This method ensures that the balance of the new investment account is non-negative 
        before proceeding with the creation. If the balance is negative, a validation error 
        is raised.

        Args:
            validated_data (dict): A dictionary of validated data for creating the investment account.

        Returns:
            InvestmentAccount: The newly created investment account instance.

        Raises:
            serializers.ValidationError: If the balance is negative.
        """

        if validated_data.get('balance') < 0:
            raise serializers.ValidationError('Balance cant be a negative')
        return super().create(validated_data)
    
    
    def update(self, instance, validated_data):
        """Update an investment account instance with validated data.
        Args:
            instance (InvestmentAccount): The investment account instance to be updated.

        Returns:
            InvestmentAccount: The updated investment account instance.

        """
        for key, value in validated_data.items():
            if key == 'balance':
                new_balance = instance.balance + value
                if new_balance < 0:
                    raise serializers.ValidationError(
                'Withdrawal amount exceeds the available balance.')
                instance.balance = new_balance
            else:
                setattr(instance, key, value)
        
        instance.save()
        return instance




class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        exclude = ['user_permissions', 'groups', 'is_superuser', 'is_active']

    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])

        return super().create(validated_data)
    

class TransactionSeializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class DateSerialializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()