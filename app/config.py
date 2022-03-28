"""
Create settings object from environment variables for use in database or oauth2.
Can get the variables from .env file.
"""

from pydantic import BaseSettings

class Settings(BaseSettings):
    """Settings object, defining variables / data type"""
    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        """Import variables from .env file, if possible"""
        env_file = ".env"

settings = Settings()
