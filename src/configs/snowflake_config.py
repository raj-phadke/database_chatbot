from pydantic import BaseModel


class SnowflakeConnectionConfig(BaseModel):
    user: str
    password: str
    account_url: str
    warehouse: str
    database: str
    db_schema: str
