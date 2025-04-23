from decouple import config

class Settings:
    TELEGRAM_API_ID = config("TELEGRAM_API_ID")
    TELEGRAM_API_HASH = config("TELEGRAM_API_HASH")
    TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")
    SECRET_KEY = config("SECRET_KEY")
    APP_URL = config("APP_URL")
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = config("AWS_REGION")
    AWS_BUCKET_NAME = config("AWS_BUCKET_NAME")
    AWS_ENDPOINT_URL = config("AWS_ENDPOINT_URL")
    AWS_PUBLIC_URL = config("AWS_PUBLIC_URL")
    DATABASE_URL = config("DATABASE_URL")
    AWS_S3_SIGNATURE_VERSION = config("AWS_S3_SIGNATURE_VERSION")

settings = Settings()
