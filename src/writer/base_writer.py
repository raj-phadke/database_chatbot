from abc import ABC, abstractmethod
from src.configs.writer_config import WriterConfig


class BaseWriter(ABC):
    def __init__(self, conn: None, config: WriterConfig) -> None:
        self.config = config
        self.conn = conn

    @abstractmethod
    def write_data(self) -> None:
        pass
