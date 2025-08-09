from ninja.security import HttpBearer
from datetime import datetime, timedelta
from usuario.models import Cliente
import jwt 


# Configurações do JWT
SECRET_KEY = "12345678910"  # Substitua por uma chave forte
ALGORITHM = "HS256"
TOKEN_EXPIRATION_MINUTES = 60


# Classe de segurança para autenticação com JWT
class JWTAuth(HttpBearer):
    def authenticate(self, request, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user = Cliente.objects.get(id=payload["user_id"])
            return user
        except (jwt.ExpiredSignatureError, jwt.DecodeError, Cliente.DoesNotExist):
            return None

auth = JWTAuth()
