import pandas as pd
from pydantic import BaseModel
from typing import Dict, Optional


class WriterConfig(BaseModel):
    dataframes: Dict[str, pd.DataFrame]
    write_path: Optional[str] = ""

    class Config:
        arbitrary_types_allowed = (
            True  # This allows non-serializable types like pd.DataFrame
        )
