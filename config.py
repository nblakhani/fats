import os
from dotenv import load_dotenv

load_dotenv()

def get_db_url():
    url = os.environ.get("DATABASE_URL", "")
    # Skip if empty or localhost (Railway shared variable default)
    if not url or "localhost" in url:
        url = "postgresql://postgres:qRYplPzRAIdZNmHxTRfxLlyMEacNSsXG@postgres.railway.internal:5432/railway"
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
    SQLALCHEMY_DATABASE_URI = get_db_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }
    EOD_REPORT_TIME = os.environ.get("EOD_REPORT_TIME", "19:00")
    WHATSAPP_API_KEY = os.environ.get("WHATSAPP_API_KEY", "")
    MANAGER_PHONE = os.environ.get("MANAGER_PHONE", "")
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}