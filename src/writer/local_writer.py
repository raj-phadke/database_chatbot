import os
from src.writer.base_writer import BaseWriter


class LocalWriter(BaseWriter):
    """
    Writer class that saves DataFrames to the local filesystem as CSVs.
    """

    def write_data(self) -> None:
        """
        Writes each DataFrame to a separate CSV file in the specified write path.
        """
        if self.config.write_path and os.path.exists(self.config.write_path):
            base_path = (
                self.config.write_path
                if self.config.write_path.endswith("/")
                else self.config.write_path + "/"
            )

            for df_name, df in self.config.dataframes.items():
                full_path = f"{base_path}{df_name}.csv"
                df.to_csv(full_path, index=False)
