import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*").split(",")

    @staticmethod
    def get_sqlalchemy_url():
        user = os.environ.get("DATABASE_USER", "postgres")
        password = os.environ.get("DATABASE_PASSWORD", "postgres")
        host = os.environ.get("DATABASE_HOST", "localhost")
        port = os.environ.get("DATABASE_PORT", "5432")
        name = os.environ.get("DATABASE_NAME", "payday")
        return f"postgresql://{user}:{password}@{host}:{port}/{name}?sslmode=require"


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://"
        f"{os.environ.get('DATABASE_USER', 'postgres')}:"
        f"{os.environ.get('DATABASE_PASSWORD', 'postgres')}@"
        f"{os.environ.get('DATABASE_HOST', 'localhost')}:"
        f"{os.environ.get('DATABASE_PORT', '5432')}/"
        f"{os.environ.get('DATABASE_NAME', 'payday_test')}"
        f"?sslmode=disable"
    )
