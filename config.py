from pydantic_settings import BaseSettings

class Settings(BaseSettings):

  SQLALCHEMY_DATABASE_URI : str = "sqlite:///foodconnect.db"
  SQLALCHEMY_TRACK_MODIFICATIONS : bool = False


def get_settings() -> Settings:
  return Settings()

settings = get_settings()