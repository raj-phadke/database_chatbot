from abc import ABC, abstractmethod
from src.configs.writer_config import WriterConfig


class BaseWriter(ABC):
    """
    Abstract base class for all writer implementations.
    """

    def __init__(self, conn: object | None, config: WriterConfig) -> None:
        """
        Initializes the writer with a connection and config.

        Args:
            conn (object | None): The connection object (e.g., SnowflakeConnection).
            config (WriterConfig): Configuration for writing data.
        """
        self.config: WriterConfig = config
        self.conn: object | None = conn

    @abstractmethod
    def write_data(self) -> None:
        """Abstract method to write data."""
        pass
