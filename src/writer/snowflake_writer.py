import pandas as pd
from snowflake.connector.pandas_tools import write_pandas
import snowflake.connector
from src.writer.base_writer import BaseWriter
from src.configs.writer_config import WriterConfig
from src.connections.snowflake_connection import SnowflakeConnection


class SnowflakeWriter(BaseWriter):
    """
    Writer class for loading data into Snowflake tables using write_pandas.
    """

    def __init__(self, conn: SnowflakeConnection, config: WriterConfig) -> None:
        """
        Initializes the writer and establishes the Snowflake connection.

        Args:
            conn (SnowflakeConnection): The Snowflake connection manager.
            config (WriterConfig): Configuration including dataframes to write.
        """
        super().__init__(conn=conn, config=config)
        self.conn.connect()

    def write_data(self) -> None:
        """
        Writes each DataFrame to its corresponding table in Snowflake.
        """
        schema = self.conn.config.db_schema.upper()
        database = self.conn.config.database.upper()

        for df_name, df in self.config.dataframes.items():
            table_name = df_name.upper()

            try:
                cursor = self.conn.connection.cursor()
                cursor.execute(f"USE DATABASE {database}")
                cursor.execute(f"USE SCHEMA {schema}")

                print(f"Writing to table: {table_name}")
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

    def _generate_create_table_sql(
        self, df: pd.DataFrame, schema_name: str, df_name: str
    ) -> str:
        """
        Generates SQL to create a table from a DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame.
            schema_name (str): The schema name.
            df_name (str): The table name.

        Returns:
            str: CREATE TABLE SQL string.
        """
        columns = ", ".join(
            [
                f'"{col}" {self._get_column_type(dtype)}'
                for col, dtype in zip(df.columns, df.dtypes)
            ]
        )
        return (
            f"CREATE TABLE IF NOT EXISTS {schema_name}.{df_name.upper()} ({columns});"
        )

    def _get_column_type(self, dtype: pd.Series.dtype) -> str:
        """
        Maps pandas dtype to Snowflake SQL data type.

        Args:
            dtype (pd.Series.dtype): Pandas data type.

        Returns:
            str: Snowflake data type.
        """
        if dtype == "int64":
            return "INTEGER"
        elif dtype == "float64":
            return "FLOAT"
        elif dtype == "object":
            return "STRING"
        elif dtype == "datetime64[ns]":
            return "TIMESTAMP"
        return "STRING"
