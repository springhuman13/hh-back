import hashlib
import hmac
from urllib.parse import urlencode
from app.core.config import settings

def verify_telegram_auth(data: dict) -> bool:
    check_hash = data.pop("hash")
    data_check_string = '\n'.join(
        f"{k}={v}" for k, v in sorted(data.items())
    )

    secret_key = hashlib.sha256(settings.TELEGRAM_BOT_TOKEN.encode()).digest()
    hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    return hmac_hash == check_hash
