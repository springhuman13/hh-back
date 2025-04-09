import hashlib
import hmac
from urllib.parse import urlencode
from decouple import config

def verify_telegram_auth(data: dict) -> bool:
    """
    Проверяет подпись Telegram по документации: https://core.telegram.org/widgets/login#checking-authorization
    """
    tg_token = config("TELEGRAM_BOT_TOKEN")

    check_hash = data.pop("hash")
    data_check_string = '\n'.join(
        f"{k}={v}" for k, v in sorted(data.items())
    )

    secret_key = hashlib.sha256(tg_token.encode()).digest()
    hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    return hmac_hash == check_hash
