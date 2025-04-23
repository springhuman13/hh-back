from fastapi import Depends, UploadFile
from sqlalchemy.orm import Session
from uuid import uuid4
import boto3
from botocore.config import Config
from botocore.exceptions import NoCredentialsError
from typing import Annotated, List

from app.models import User, Certificate
from app.schemas.certificate import CertificateOut
from app.core.config import settings
from app.database import get_db


class S3Service:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_ENDPOINT_URL,
        )
        self.bucket = settings.AWS_BUCKET_NAME

    def upload_file(self, file: UploadFile, user_id: int, db: Session) -> dict:
        key = f"{user_id}/{uuid4()}_{file.filename}"

        self.s3.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=file.file,
        )

        url = f"{settings.AWS_PUBLIC_URL}/{self.bucket}/{key}"

        certificate = Certificate(
            user_id=user_id,
            original_filename=file.filename,
            s3_key=key,
            s3_url=url,
        )
        db.add(certificate)
        db.commit()

    def _generate_presigned_url(self, bucket_name: str, object_key: str, expiration: int = 3600) -> str:
        try:
            url = self.s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': object_key},
                ExpiresIn=expiration
            )
            return url
        except NoCredentialsError:
            print("Ошибка: Нет учетных данных для доступа к S3.")
            return ''
        except Exception as e:
            print(f"Ошибка при генерации ссылки: {e}")
            return ''

    def get_all(self, user: User, db: Session) -> list[CertificateOut]:
        files = db.query(Certificate).filter(Certificate.user_id == user.id).all()
        certificates_out = []
        for file in files:
            download_url = self._generate_presigned_url(self.bucket, file.s3_key)
            certificates_out.append(CertificateOut(id=file.id, original_filename=file.original_filename, download_url=download_url))

        return certificates_out

S3ServiceDep = Annotated[S3Service, Depends()]
