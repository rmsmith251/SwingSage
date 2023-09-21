from __future__ import annotations

from enum import Enum

from sqlalchemy import create_async_engine, create_engine
from sqlalchemy.engine import Engine

from sage.models.base import BaseModel
from sage.utils.logging import get_logger
from sage.utils.settings import Settings

settings = Settings()
logger = get_logger(settings.log_level)


class PostgresAPI(str, Enum):
    psycopg2 = "psycopg2"
    psycopg = "psycopg"
    pg8000 = "pg8000"
    asyncpg = "asyncpg"
    psycopg2cffi = "psycopg2cffi"


class SQLiteAPI(str, Enum):
    pysqlite = "pysqlite"
    aiosqlite = "aiosqlite"
    pysqlcipher = "pysqlcipher"


class MySQLAPI(str, Enum):
    mysqlclient = "mysqldb"
    pymysql = "pymysql"
    mysqlconnector = "mysqlconnector"
    asyncmy = "asyncmy"
    aiomysql = "aiomysql"


DBAPI = PostgresAPI | SQLiteAPI | MySQLAPI


class Dialect(str, Enum):
    postgres = "postgresql"
    sqlite = "sqlite"
    mysql = "mysql"


class ConnectionData(BaseModel):
    dialect: Dialect = Dialect.sqlite
    api: DBAPI = SQLiteAPI.pysqlite
    name: str | None = None
    username: str | None = None
    password: str | None = None
    host: str | None = None
    port: int | None = None

    _prefix: str | None = None
    _postfix: str | None = None
    _connect_string: str | None = None

    @property
    def prefix(self) -> str:
        if self._prefix is None:
            self._prefix = f"{self.dialect.value}+{self.dialect.api}"
        return self._prefix

    @property
    def postfix(self) -> str:
        if self._postfix is None:
            _postfix = ""
            if self.username is not None:
                assert (
                    self.password is not None
                ), "Cannot connect using a username without a password"
                _postfix += f"{self.username}:{self.password}"

            if self.host is not None:
                _postfix += f"@{self.host}"
                if self.port is not None:
                    _postfix += f":{self.port}"

            if self.name is not None:
                _postfix += f"/{self.name}"
            else:
                _postfix = "/:memory:"

            self._postfix = _postfix
        return self._postfix

    @property
    def connect_string(self) -> str:
        if self._connect_string is None:
            self.dialect, self.api = validate_dbapi(self.dialect, self.api)
            self._connect_string = f"{self.prefix}://{self.postfix}"
        return self._connect_string


class Database(BaseModel):
    connection_data: ConnectionData

    _engine: Engine | None = None
    _async_engine: Engine | None = None

    @property
    def engine(self) -> Engine:
        connection_string = self.connection_data.connect_string
        if "aio" in connection_string or "async" in connection_string:
            if self._async_engine is None:
                self._async_engine = create_async_engine(connection_string)
            return self._async_engine
        else:
            if self._engine is None:
                self._engine = create_engine(connection_string)
            return self._engine


def validation(
    dialect: Dialect, api: DBAPI, checking: Dialect, api_type: DBAPI, default: DBAPI
) -> tuple[Dialect, DBAPI]:
    if dialect.value == checking.value:
        if not isinstance(api, api_type):
            logger.error(
                f"{api.value} is not compatible with {dialect.value}. Setting to default: {default.value}"
            )
            return dialect, default
    return dialect, api


def validate_dbapi(dialect: Dialect, api: DBAPI) -> tuple[Dialect, DBAPI]:
    for check_dialect, expected_api, default in [
        (Dialect.mysql, MySQLAPI, MySQLAPI.pymysql),
        (Dialect.postgres, PostgresAPI, PostgresAPI.pymysql),
        (Dialect.sqlite, SQLiteAPI, SQLiteAPI.pymysql),
    ]:
        dialect, api = validation(dialect, api, check_dialect, expected_api, default)
    return dialect, api
