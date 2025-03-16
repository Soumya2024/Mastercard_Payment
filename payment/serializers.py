# payment/serializers.py
from rest_framework import serializers

class PaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3)
    card_number = serializers.CharField(max_length=19)
    expiry_date = serializers.CharField(max_length=5)  # MM/YY format
    cvv = serializers.CharField(max_length=4)
