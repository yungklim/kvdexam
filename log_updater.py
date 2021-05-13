
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union

from log_item import LogItem


class LogUpdater(ABC):

    @abstractmethod
    def update(self, message_list: List[LogItem]) -> None:
        pass

    @abstractmethod
    def read(self, log_date: str, time_interval: Optional[Tuple[str, str]] = None) -> List[Dict[str, Union[datetime, str]]]:
        pass

    @abstractmethod
    def flush(self, from_date: Optional[str] = None) -> None:
        pass