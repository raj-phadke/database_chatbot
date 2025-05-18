import os
from src.writer.base_writer import BaseWriter


class LocalWriter(BaseWriter):
    def write_data(self) -> None:
        if self.config.write_path and os.path.exists(self.config.write_path):
            for df_name, df in self.config.dataframes.items():
                cleaned_base_path = (
                    self.config.write_path
                    if self.config.write_path[-1] == "/"
                    else self.config.write_path + "/"
                )

                full_write_path = cleaned_base_path + df_name

                df.to_csv(full_write_path, index=False)

        return
