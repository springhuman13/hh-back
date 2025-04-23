from pydantic import BaseModel

# === CERTIFICATE ===
class CertificateOut(BaseModel):
    id: int
    original_filename: str
    download_url: str

    model_config = {
        "from_attributes": True
    }