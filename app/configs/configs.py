from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME:str
    VERSION:str
    ENVIRONMENT:str
    POSTGRESQL_HOST:str
    POSTGRESQL_PORT:str
    POSTGRESQL_USER:str
    POSTGRESQL_PASSWORD:str
    POSTGRESQL_DBNAME:str
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore" 
    )

settings = Settings()