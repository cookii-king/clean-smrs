from ...models import Price
from decimal import Decimal
from rest_framework import serializers

class PriceSerializer(serializers.ModelSerializer):
    unit_amount = serializers.DecimalField(max_digits=10, decimal_places=2)  # Input as decimal
    recurring = serializers.JSONField(required=False, allow_null=True)  # Accept JSON data directly

    class Meta:
        model = Price
        fields = ['id', 'currency', 'unit_amount', 'recurring', 'product', 'stripe_price_id']
        read_only_fields = ['stripe_price_id']
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    
    def validate_unit_amount(self, value):
        """
        Validate and convert unit_amount to an integer for Stripe (in cents).
        """
        if value <= 0:
            raise serializers.ValidationError("The amount must be greater than zero.")
        return int(Decimal(value) * 100)  # Convert to integer cents
    
    # def validate_recurring(self, value):
    #     """
    #     Validate the recurring field to ensure it is a valid JSON object.
    #     """
    #     if value:
    #         if not isinstance(value, dict):
    #             raise serializers.ValidationError("The 'recurring' field must be a valid JSON object.")
            
    #         interval = value.get('interval')
    #         aggregate_usage = value.get('aggregate_usage')

    #         # Validate `interval`
    #         if interval and interval not in ['day', 'week', 'month', 'year']:
    #             raise serializers.ValidationError("Invalid 'interval'. Must be one of: day, week, month, year.")

    #         # Validate `aggregate_usage`
    #         if aggregate_usage and aggregate_usage not in ['sum', 'last_during_period', 'last_ever', 'max']:
    #             raise serializers.ValidationError(
    #                 "Invalid 'aggregate_usage'. Must be one of: sum, last_during_period, last_ever, max."
    #             )
    #     return value

    def to_representation(self, instance):
        """
        Ensure unit_amount is represented as an integer in the output.
        """
        representation = super().to_representation(instance)
        representation['unit_amount'] = instance.unit_amount  # Show the raw integer
        return representation