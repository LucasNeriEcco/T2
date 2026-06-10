import os
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-secreta-boosting-2026")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:963968@127.0.0.1:3306/boosting_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
