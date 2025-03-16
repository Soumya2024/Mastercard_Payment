from django.shortcuts import render
import json
import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PaymentSerializer

# Create your views here.
class PaymentView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            # Get the validated data
            amount = serializer.validated_data['amount']
            currency = serializer.validated_data['currency']
            card_number = serializer.validated_data['card_number']
            expiry_date = serializer.validated_data['expiry_date']
            cvv = serializer.validated_data['cvv']
            
            # Prepare data for Mastercard API request
            payment_data = {
                'amount': amount,
                'currency': currency,
                'card_number': card_number,
                'expiry_date': expiry_date,
                'cvv': cvv,
                # Additional data such as merchant id, etc.
                'merchant_id': settings.MASTERCARD_MERCHANT_ID,
            }
            
            # Make the POST request to the Mastercard API
            headers = {
                'Authorization': f'Bearer {settings.MASTERCARD_API_KEY}',
                'Content-Type': 'application/json'
            }

            try:
                response = requests.post(settings.MASTERCARD_API_URL, 
                                         json=payment_data, 
                                         headers=headers)
                
                # Check response from Mastercard
                if response.status_code == 200:
                    return Response(response.json(), status=status.HTTP_200_OK)
                else:
                    return Response(response.json(), status=status.HTTP_400_BAD_REQUEST)
            
            except requests.exceptions.RequestException as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# {
#     "amount": 100.00,
#     "currency": "USD",
#     "card_number": "4111111111111111",
#     "expiry_date": "12/25",
#     "cvv": "123"
# }
