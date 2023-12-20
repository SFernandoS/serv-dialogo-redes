import jwt
from datetime import datetime, timedelta

class JWTManager:
    secret_key = "seu_segredo_super_secreto"

    @staticmethod
    def encode_token(data):
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=30),
            'iat': datetime.utcnow(),
            **data
        }
        return jwt.encode(payload, JWTManager.secret_key, algorithm='HS256')

    @staticmethod
    def decode_token(token):
        try:
            if token.startswith("Bearer "):
                token = token[len("Bearer "):]
            payload = jwt.decode(token, JWTManager.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return "Token expirado. Faça login novamente."
        except jwt.InvalidTokenError:
            return "Token inválido. Faça login novamente."
