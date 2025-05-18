import snowflake.connector
from snowflake.connector.connection import SnowflakeConnection
from src.configs.snowflake_config import SnowflakeConnectionConfig


class SnowflakeConnection:
    def __init__(self, config: SnowflakeConnectionConfig) -> None:
        self.config = config
        self.connection = None  # This will store the actual Snowflake connection object

    def connect(self) -> None:
        try:
            # Create the Snowflake connection and store it in self.connection
            self.connection = snowflake.connector.connect(
                user=self.config.user,
                password=self.config.password,
                account=self.config.account_url,  # E.g. abcd-xy12345.snowflakecomputing.com (omit https)
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
        # Ensure that the connection is closed properly when disconnecting
        if self.connection is not None:
            self.connection.close()
            print("🔒 Snowflake connection closed.")
