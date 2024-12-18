from ...models import Plan
from decimal import Decimal
from rest_framework import serializers

class PlanSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)  # Input as decimal

    class Meta:
        model = Plan
        fields = ['id', 'currency', 'interval', 'product', 'amount', 'stripe_plan_id']
        read_only_fields = ['stripe_plan_id']
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    
    def validate_amount(self, value):
        """
        Validate and convert amount to an integer for Stripe (in cents).
        """
        if value <= 0:
            raise serializers.ValidationError("The amount must be greater than zero.")
        return int(Decimal(value) * 100)  # Convert to integer cents
    

    def to_representation(self, instance):
        """
        Ensure amount is represented as an integer in the output.
        """
        representation = super().to_representation(instance)
        representation['amount'] = instance.amount  # Show the raw integer
        return representation