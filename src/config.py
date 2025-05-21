from dataclasses import dataclass
from typing import Optional

from sqlalchemy.engine.url import URL
from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    port: int

    def construct_sqlalchemy_url(self, driver="asyncpg", host=None, port=None) -> str:
        if not host:
            host = self.host
        if not port:
            port = self.port
        uri = URL.create(
            drivername=f"postgresql+{driver}",
            username=self.user,
            password=self.password,
            host=host,
            port=port,
            database=self.database,
        )
        return uri.render_as_string(hide_password=False)

    @staticmethod
    def from_env(env: Env):
        host = env.str("DB_HOST")
        password = env.str("POSTGRES_PASSWORD")
        user = env.str("POSTGRES_USER")
        database = env.str("POSTGRES_DB")
        port = env.int("DB_PORT")
        return DbConfig(
            host=host, password=password, user=user, database=database, port=port
        )


@dataclass
class AppConfig:
    port: int = 8000
    cors_origins: list[str] = None

    @staticmethod
    def from_env(env: Env):
        port = env.int("APP_PORT", default=8000)
        cors_origins = env.list("CORS_ORIGINS", subcast=str, default=["*"])
        return AppConfig(
            port=port,
            cors_origins=cors_origins
        )


@dataclass
class Config:
    db: Optional[DbConfig]
    app: AppConfig


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        db=DbConfig.from_env(env),
        app=AppConfig.from_env(env),
    )


config = load_config(".env")
