from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    CLIENT_ID: str
    CLIENT_SECRET: str
    PG_HOST: str
    PG_PORT: str
    PG_USER: str
    PG_PASS: str
    PG_DATABASE: str
    DB_DIALECT: str = "postgresql+asyncpg"

    @property
    def db_url(self) -> str:
        return (
            f"{self.DB_DIALECT}://{self.PG_USER}:{self.PG_PASS}@{self.PG_HOST}:"
            f"{self.PG_PORT}/{self.PG_DATABASE}"
        )

    class Config:
        env_file = ".env"


settings = Settings()
