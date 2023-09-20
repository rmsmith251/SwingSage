from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    user: str
    contact_email: str
    log_level: str = "INFO"
