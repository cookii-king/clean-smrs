from ...models import Account
from rest_framework import serializers

from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for the Account model.
    """
    # Ensure password is write-only and not exposed in the response
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Account
        fields = [
            'id',
            'username',
            'name',
            'email',
            'description',
            'email_confirmed',
            'mfa_enabled',
            'stripe_customer_id',
            'created',
            'updated',
            'deleted',
            'password'
        ]
        read_only_fields = ['id', 'email_confirmed', 'stripe_customer_id', 'created', 'updated', 'deleted']

    def validate_password(self, value):
        """
        Hash the password before saving to the database.
        """
        return make_password(value)

    def create(self, validated_data):
        """
        Handle creation of a new Account.
        """
        password = validated_data.pop('password', None)
        account = Account(**validated_data)
        if password:
            account.password = make_password(password)
        account.save()
        return account

    def update(self, instance, validated_data):
        """
        Handle updating an Account.
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.password = make_password(password)
        instance.save()
        return instance
