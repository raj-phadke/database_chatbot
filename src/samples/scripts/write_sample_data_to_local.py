from src.samples.scripts.generate_sample_dw_data import generate_sample_data
from src.writer.local_writer import LocalWriter
from src.configs.writer_config import WriterConfig

sample_data = generate_sample_data()

write_config = WriterConfig(dataframes=sample_data, write_path="src/samples/data/")

writer_instance = LocalWriter(conn=None, config=write_config)
writer_instance.write_data()
