import functools
import logging
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union

from log_item import LogItem
from log_updater import LogUpdater

logger = logging.getLogger(__name__)


def db_logging(log_statement: str):

    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            try:
                result_or_none = function(*args, **kwargs)
                logger.info(
                    "%s - успешно: %s.\nАргументы:%s, %s",
                    function.__name__,
                    log_statement,
                    str(args)[:100],
                    str(kwargs)[:100],
                )
                return result_or_none
            except Exception as error:
                logger.error(
                    "%s - ОШИБКА: %s.\n%s\nАргументы:%s, %s",
                    function.__name__,
                    log_statement,
                    str(error),
                    str(args)[:100],
                    str(kwargs)[:100],
                )
                raise

        return wrapper

    return decorator


class Database(LogUpdater):

    def __init__(self, db_uri: str) -> None:
        
        self.db_uri = db_uri
        self._connect_to_db(self.db_uri)

    @db_logging("подключение к бд")
    def _connect_to_db(self, db_uri: str) -> None:
        self.connection: sqlite3.Connection = sqlite3.connect(
            db_uri, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        self.connection.row_factory = sqlite3.Row
        self.cursor: sqlite3.Cursor = self.connection.cursor()

    @db_logging("обновление информации бд")
    def update(self, message_list: List[LogItem]) -> None:

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS log_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at timestamp NOT NULL,
                first_name TEXT,
                message TEXT,
                second_name TEXT,
                user_id TEXT NOT NULL,
                
                CONSTRAINT fk_users
                    FOREIGN KEY (user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
            );
            """
        )
        
        self.connection.commit()

        for element in message_list:

            self.cursor.execute(
                """
                INSERT INTO 'log_messages'
                    ('created_at', 'first_name', 'message', 'second_name', 'user_id' )
                VALUES (?, ?, ?, ?, ?);
                """,
                (
                    element.created_at,
                    element.first_name,
                    element.message,
                    element.second_name,
                    element.user_id,
                    
                ),
            )
        self.connection.commit()

    @db_logging("получение информации из логов")
    def read(
        self, log_date: str, time_interval: Optional[Tuple[str, str]] = None
    ) -> List[Dict[str, Union[datetime, str]]]:
        time_boundaries: Tuple[datetime, datetime]

        if time_interval:
            time_boundaries = (
                datetime.fromisoformat(f"{log_date}T{time_interval[0]}"),
                datetime.fromisoformat(f"{log_date}T{time_interval[1]}"),
            )
        else:
            time_boundaries = (
                datetime.fromisoformat(f"{log_date}"),
                datetime.fromisoformat(f"{log_date}") + timedelta(days=1),
            )

        

        return [dict(item) for item in self.cursor.fetchall()]
    def flush(self, from_date: Optional[str] = None) -> None:

        if from_date:
            self.cursor.execute(
                """
                DELETE FROM log_messages
                WHERE created_at > ? ;
                """,
                (datetime.fromisoformat(from_date)),
            )
        else:
            self.cursor.execute(
                """
                DELETE FROM log_messages;
                """
            )
        self.connection.commit()