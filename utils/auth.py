from ninja.security import HttpBearer
from datetime import datetime, timedelta
from usuario.models import Usuario
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
            usuario = Usuario.objects.get(id=payload["user_id"])
            return usuario
        except (jwt.ExpiredSignatureError, jwt.DecodeError, Usuario.DoesNotExist):
            return None

auth = JWTAuth()
