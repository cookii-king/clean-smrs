from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from django.shortcuts import render, redirect
import stripe
import os
from dotenv import load_dotenv
load_dotenv()

STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')

stripe.api_key = STRIPE_SECRET_KEY

class PaymentLinksView(APIView):
    def post(self, request):
        response =  stripe.PaymentLink.create(
        after_completion=[],
        line_items=[{"price": "price_1QScDZLqX3boq1N3kgVWLdm3", "quantity": 1}],
        
        )
        # print(response)
        return Response(data={"response": response})
        # # Delete the JWT cookie
        # response = redirect('/')  # Redirects to the homepage (/)
        # response.delete_cookie('jwt')  # Delete the JWT token cookie
        # return response
        # return redirect(response.url)

    def get(self, request):
        pass
        # # Delete the JWT cookie
        # response = redirect('/')  # Redirects to the homepage (/)
        # response.delete_cookie('jwt')  # Delete the JWT token cookie
        # return response
    