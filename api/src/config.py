from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    CLIENT_ID: str
    CLIENT_SECRET: str
    OAUTH_TOKEN: str
    REDIRECT_URI: str

    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_ROOT_PASSWORD: str

    @property
    # For alembic migration
    def get_sync_mysql_url(self):
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

    @property
    # For application handler
    def get_async_mysql_url(self):
        return f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
