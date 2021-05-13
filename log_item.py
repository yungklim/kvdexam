from datetime import datetime

from pydantic import BaseModel


class LogItem(BaseModel):
    user_id: str
    created_at: datetime
    first_name: str
    second_name: str
    message: str
