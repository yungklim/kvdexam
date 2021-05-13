import argparse
import json
import logging
import sys
from pathlib import Path

import database, log_receiver

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%y-%m-%d %H:%M:%S",
    filename="exam_log.log",
)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title="commands", dest="command")

parser_fetch = subparsers.add_parser(
    "fetch", help="получить логи с помощью API для определенной даты"
)
parser_fetch.add_argument("base_url", type=str, help="URL для получения логов")
parser_fetch.add_argument("date_path", type=str, help="Формат лога в ГГГММДД")
parser_fetch.add_argument(
    "db_file",
    nargs="?",
    type=Path,
    help="Файл БД. Стандартн. - database.db",
    default=Path("database.db"),
)


parser_show = subparsers.add_parser(
    "show",
    help="Печать сохр. даты логов для желаемой даты и интервала в NDJSON формате",
)
parser_show.add_argument(
    "date", type=str, help="Дата логов. Формат - ГГГГММДД"
)
parser_show.add_argument(
    "db_file",
    nargs="?",
    type=Path,
    help="Файл БД. Стандартн. - database.db",
    default=Path("database.db"),
)
parser_show.add_argument(
    "-i", "--interval", type=str, help="Формат времени. ЧЧ:ММ:СС - ЧЧ:ММ:СС"
)

args = parser.parse_args()



if args.command == "fetch":
    print("Получаем логи за определенную дату...")
    try:
        get_logs = log_receiver.LogReceiver(args.base_url)
        db = database.Database(args.db_file)
        db.update(get_logs(args.date_path))
        print("Выполнено")
    except Exception as error:
        logging.exception(error)
        sys.exit(
            f"Ошибка в получении логов. Ошибка: {str(error)}\nДоп. информация в файле лога."
        )
elif args.command == "show":
    if not args.db_file.exists():
        sys.exit(f"Файл БД ({args.db_file}) не существует")
    try:
        db = database.Database(args.db_file)
        time_interval = tuple(args.interval.split("-")) if args.interval else None
        for element in db.read(args.date, time_interval):
            element.created_at = str(element.created_at)
            print(json.dumps(element, ensure_ascii=False))
    except Exception as error:
        logging.exception(error)
        sys.exit(
            f"Ошибка в чтении логов из БД: {str(error)}\nДоп информация в файле лога."
        )