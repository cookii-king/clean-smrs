from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

class IndexView(APIView):
    def post(self, request):
        try:
            return Response()
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for IndexView: {e}"}, status=400)
    
    def get(self, request):
        try:
            account = request.user
            return render(request, 'index.html', {'account':account})
        except Exception as e:
            return Response(data={"error": f"'GET' Method Failed for IndexView: {e}"}, status=400)

class AboutView(APIView):
    def post(self, request):
        try:
            return Response()
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for AboutView: {e}"}, status=400)
    
    def get(self, request):
        try:
            account = request.user
            return render(request, 'about.html', {'account':account})
        except Exception as e:
            return Response(data={"error": f"'GET' Method Failed for AboutView: {e}"}, status=400)

class ContactView(APIView):
    def post(self, request):
        try:
            if request.path == '/contact/submit':
                pass
            return Response()
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for ContactView: {e}"}, status=400)
    
    def get(self, request):
        try:
            account = request.user
            return render(request, 'contact.html', {'account':account})
        except Exception as e:
            return Response(data={"error": f"'GET' Method Failed for ContactView: {e}"}, status=400)

class SupportView(APIView):
    def post(self, request):
        try:
            if request.path == '/support/submit':
                pass
            return Response()
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for SupportView: {e}"}, status=400)
    
    def get(self, request):
        try:
            account = request.user
            return render(request, 'support.html', {'account':account})
        except Exception as e:
            return Response(data={"error": f"'GET' Method Failed for SupportView: {e}"}, status=400)

class TermsOfServiceView(APIView):
    def post(self, request):
        try:
            return Response()
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for TermsOfServiceView: {e}"}, status=400)
    
    def get(self, request):
        try:
            account = request.user
            return render(request, 'terms-of-service.html', {'account':account})
        except Exception as e:
            return Response(data={"error": f"'GET' Method Failed for TermsOfServiceView: {e}"}, status=400)

class PrivacyPolicyView(APIView):
    def post(self, request):
        try:
            return Response()
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for PrivacyPolicyView: {e}"}, status=400)
    
    def get(self, request):
        try:
            account = request.user
            return render(request, 'privacy-policy.html', {'account':account})
        except Exception as e:
            return Response(data={"error": f"'GET' Method Failed for PrivacyPolicyView: {e}"}, status=400)
