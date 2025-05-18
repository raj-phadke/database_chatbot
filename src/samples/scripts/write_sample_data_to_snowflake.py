from src.samples.scripts.generate_sample_dw_data import generate_sample_data
from src.configs.writer_config import WriterConfig
from src.connections.snowflake_connection import SnowflakeConnection
from src.configs.snowflake_config import SnowflakeConnectionConfig
from src.writer.snowflake_writer import SnowflakeWriter

sample_data = generate_sample_data()

write_config = WriterConfig(dataframes=sample_data, write_path="")

snowflake_config = SnowflakeConnectionConfig(
    user="RRPHADKE10",
    password="Iamlazybatman100296!",
    account_url="mv38776.us-east4.gcp",  # ✅ Corrected account with region
    warehouse="COMPUTE_WH",
    database="RETAIL_DW",
    db_schema="SALES",
)

snowflake_connection = SnowflakeConnection(config=snowflake_config)
print(snowflake_connection)

writer_instance = SnowflakeWriter(conn=snowflake_connection, config=write_config)
writer_instance.write_data()
