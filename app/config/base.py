from pydantic import BaseSettings, PostgresDsn, RedisDsn


ENV_FILE_PATH = ".env"


class AppSettings(BaseSettings):
    class Config:
        env_file: str = ENV_FILE_PATH

    host: str = "localhost"
    port: int = 8000


class PostgreSQL(BaseSettings):
    __separator = "://"

    class Config:
        env_file: str = ENV_FILE_PATH
        env_prefix: str = "POSTGRESQL"

    dsn: PostgresDsn = "postgres://user:password@127.0.0.1:5432/db"

    def build_using_new_scheme(self, scheme: str) -> str:
        return f"{self.__separator}".join(
            [scheme, self.dsn.split(sep=self.__separator)[1]]
        )

    @property
    def using_async_driver(self):
        return self.build_using_new_scheme("postgresql+asyncpg")


class Redis(BaseSettings):
    class Config:
        env_file: str = ENV_FILE_PATH
        env_prefix: str = "REDIS_"

    dsn: RedisDsn = "redis://username:password@localhost:6379/0"


class Config(BaseSettings):
    app: AppSettings
    postgresql: PostgreSQL
    redis: Redis

    @classmethod
    def create(cls):
        return Config(app=AppSettings(), postgresql=PostgreSQL(), redis=Redis())
