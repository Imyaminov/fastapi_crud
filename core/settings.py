from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_PORT: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str

    CLIENT_ORIGIN: str

    VERIFICATION_SECRET: str

    class Config:
        env_file = 'crud_app/.env'


settings = Settings()