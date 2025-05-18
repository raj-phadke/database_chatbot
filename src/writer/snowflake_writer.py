import pandas as pd
from snowflake.connector.pandas_tools import write_pandas
import snowflake.connector
from src.writer.base_writer import BaseWriter
from src.configs.writer_config import WriterConfig
from src.connections.snowflake_connection import SnowflakeConnection


class SnowflakeWriter(BaseWriter):
    def __init__(self, conn: SnowflakeConnection, config: WriterConfig) -> None:
        super().__init__(conn=conn, config=config)
        self.conn.connect()  # Make sure to connect before using it

    def write_data(self) -> None:
        # Accessing db_schema correctly from the config of SnowflakeConnection (conn)
        schema_name = (
            self.conn.config.db_schema.upper()
        )  # Make sure schema is uppercase
        database_name = (
            self.conn.config.database.upper()
        )  # Make sure database is uppercase

        for df_name, df in self.config.dataframes.items():
            # Fully-qualified table name, but we will pass only the table name to write_pandas
            table_name = df_name.upper()

            try:
                # Ensure the correct database and schema are in context
                self.conn.connection.cursor().execute(f"USE DATABASE {database_name}")
                self.conn.connection.cursor().execute(f"USE SCHEMA {schema_name}")

                # Now write the data to the table using just the table name (no database/schema)
                print(f"Writing to table: {table_name}")  # Debugging step
                success, nchunks, nrows, _ = write_pandas(
                    self.conn.connection, df, table_name, auto_create_table=True
                )
                if success:
                    print(f"✅ Successfully wrote {nrows} rows to {table_name}")
                else:
                    print(f"❌ Failed to write data to {table_name}")

            except snowflake.connector.errors.ProgrammingError as e:
                print(f"❌ Snowflake SQL error while writing {table_name}: {e}")
            except Exception as ex:
                print(f"❌ General error: {ex}")
        return

    def _generate_create_table_sql(
        self, df: pd.DataFrame, schema_name: str, df_name: str
    ) -> str:
        """Generate the CREATE TABLE SQL dynamically from the DataFrame"""
        columns = ", ".join(
            [
                f'"{col}" {self._get_column_type(dtype)}'
                for col, dtype in zip(df.columns, df.dtypes)
            ]
        )
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {schema_name}.{df_name.upper()} (
            {columns}
        );
        """
        return create_table_sql

    def _get_column_type(self, dtype: pd.Series.dtype) -> str:
        """Map pandas dtypes to Snowflake SQL types"""
        if dtype == "int64":
            return "INTEGER"
        elif dtype == "float64":
            return "FLOAT"
        elif dtype == "object":
            return "STRING"
        elif dtype == "datetime64[ns]":
            return "TIMESTAMP"
        else:
            return "STRING"
