import io
import pyotp
import base64
import qrcode
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from ..authentication.view import JWTAuthentication, IsAuthenticated

class AccountView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            return Response()
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for AccountView: {e}"}, status=400)
    
    def get(self, request):
        try:
            account = request.user
            token = request.COOKIES.get('jwt')
            if(account.mfa_secret == None):
                account.generate_mfa_secret_secret()
            
            otp_uri = pyotp.totp.TOTP(account.mfa_secret).provisioning_uri(
                name=account.email,
                issuer_name="Clean SMRs"
            )

            qr = qrcode.make(otp_uri)
            buffer = io.BytesIO()
            qr.save(buffer, format="PNG")

            buffer.seek(0)
            qr_code = base64.b64encode(buffer.getvalue()).decode("utf-8")

            qr_code_data_uri = f"data:image/png;base64,{qr_code}"


            return render(request, 'account.html', {'account':account, 'token': token, 'qrcode': qr_code_data_uri})
        except Exception as e:
            return Response(data={"error": f"'GET' Method Failed for AccountView: {e}"}, status=400)
