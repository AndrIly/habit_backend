from urllib.parse import parse_qsl
import hmac
import hashlib
from datetime import datetime, timezone, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from config_data.config import ACCESS_TOKEN_EXPIRATION, JWT_ALG, JWT_SECRET
import jwt

bearer = HTTPBearer(auto_error=False)

def verify_telegram_init_data(init_data: str, bot_token: str) -> bool:
    if not bot_token:
        raise Exception('Бот токен не указан')

    data = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = data.pop('hash', None)
    if not received_hash:
        raise Exception('Нет хэша в initData')

    data_check_string = '\n'.join(f'{k} ={v}' for k, v in sorted(data.items()))

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        raise Exception('Недействительный initData хэш')
    return data


def create_access_token(tg_user_id: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        'sub': str(tg_user_id),
        'iat': int(now.timestamp()),
        'exp': int(now + timedelta(minutes=ACCESS_TOKEN_EXPIRATION)).timestamp(),
    }
    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALG,
    )


def get_current_user_id(creds: HTTPAuthorizationCredentials = Depends(bearer)):
    if not creds:
        raise HTTPException(status_code=401, detail='Missing token')
    try:
        payload = jwt.decode(creds.credentials, JWT_SECRET, algorithms=[JWT_ALG])
        return int(payload['sub'])
    except Exception:
        raise HTTPException(status_code=401, detail='Invalid token')