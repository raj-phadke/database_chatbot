import snowflake.connector
from snowflake.connector.connection import (
    SnowflakeConnection as SnowflakeConnectionType,
)
from src.configs.snowflake_config import SnowflakeConnectionConfig


class SnowflakeConnection:
    """Manages connection to a Snowflake database."""

    def __init__(self, config: SnowflakeConnectionConfig) -> None:
        """
        Initializes the SnowflakeConnection with the given configuration.

        Args:
            config (SnowflakeConnectionConfig): Configuration parameters for connecting to Snowflake.
        """
        self.config: SnowflakeConnectionConfig = config
        self.connection: SnowflakeConnectionType | None = None

    def connect(self) -> None:
        """
        Establishes a connection to the Snowflake database and stores it in self.connection.
        """
        try:
            self.connection = snowflake.connector.connect(
                user=self.config.user,
                password=self.config.password,
                account=self.config.account_url,
                warehouse=self.config.warehouse,
                database=self.config.database,
                schema=self.config.db_schema,
            )
            print("✅ Connected to Snowflake successfully!")
        except snowflake.connector.errors.Error as e:
            print("🚨 Snowflake connection error:", e)
        except Exception as ex:
            print("❌ General error:", ex)

    def disconnect(self) -> None:
        """
        Closes the connection to the Snowflake database, if one exists.
        """
        if self.connection is not None:
            self.connection.close()
            print("🔒 Snowflake connection closed.")
