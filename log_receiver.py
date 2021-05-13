from datetime import datetime
from os import path
from typing import Dict, List, Optional, Union

import requests

from log_item import LogItem
from sort import sort

LOG_LIST_NAME = "logs"
ERROR_NAME = "error"


class RequestError(Exception):

    pass


class LogReceiver:

    def __init__(self, base_url: str):
        self.base_url: str = base_url

    def __call__(
        self, date_string: str, sort_by_time: Optional[bool] = True
    ) -> List[Dict[str, Union[datetime, str]]]:
        try:
            response = requests.get(path.join(self.base_url, date_string))
            response.raise_for_status()
        except Exception as error:
            raise RequestError(str(error))

        data = response.json()
        if data[ERROR_NAME]:
            raise ValueError(data[ERROR_NAME])

        log_list = list(map(LogItem.parse_obj, data[LOG_LIST_NAME]))

        if sort_by_time:
            sort(log_list, key=lambda x: x.created_at)

        return log_list
