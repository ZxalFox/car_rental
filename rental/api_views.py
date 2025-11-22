from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CustomerSerializer


@method_decorator(ensure_csrf_cookie, name="dispatch")
class SessionView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            serializer = CustomerSerializer(request.user, context={"request": request})
            return Response({"authenticated": True, "user": serializer.data})
        return Response({"authenticated": False})


@method_decorator(ensure_csrf_cookie, name="dispatch")
class SessionLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username", "").strip()
        password = request.data.get("password", "")
        if not username or not password:
            return Response(
                {"detail": "Informe usuário e senha."}, status=status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {"detail": "Credenciais inválidas."}, status=status.HTTP_400_BAD_REQUEST
            )
        login(request, user)
        serializer = CustomerSerializer(user, context={"request": request})
        return Response({"authenticated": True, "user": serializer.data})


class SessionLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
