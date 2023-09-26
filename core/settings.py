from decouple import config
# from pydantic import BaseSettings


from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = 'CRUD'
    DATABASE_PORT: str = config('DATABASE_PORT')
    POSTGRES_PASSWORD: str = config('POSTGRES_PASSWORD')
    POSTGRES_USER: str = config('POSTGRES_USER')
    POSTGRES_DB: str = config('POSTGRES_DB')
    POSTGRES_HOST: str = config('POSTGRES_HOST')
    POSTGRES_HOSTNAME: str = config('POSTGRES_HOSTNAME')
    CLIENT_ORIGIN: str = config('CLIENT_ORIGIN')

    JWT_PUBLIC_KEY: str = config('JWT_PUBLIC_KEY')
    JWT_PRIVATE_KEY: str = config('JWT_PRIVATE_KEY')
    REFRESH_TOKEN_EXPIRES_IN: int = config('REFRESH_TOKEN_EXPIRES_IN')
    ACCESS_TOKEN_EXPIRES_IN: int = config('ACCESS_TOKEN_EXPIRES_IN')
    JWT_ALGORITHM: str = config('JWT_ALGORITHM')

    class Config:
        env_file = 'crud_app/.env'


settings = Settings()
