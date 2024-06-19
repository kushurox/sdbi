import sqlite3
import tomllib
from typing import Dict
import os

DB_PATH = f"{os.getcwd()}/server.db"
CONFIG_PATH = f"{os.getcwd()}/config.toml"


class InitDb:
    def __init__(self):
        print("DB PATH:", DB_PATH)
        print("CONFIG PATH:", CONFIG_PATH)
        self.data: Dict[str, list]
        with sqlite3.connect(DB_PATH) as self.db:
            self.cursor = self.db.cursor()

            with open(CONFIG_PATH, "rb") as fp:
                self.data = tomllib.load(fp)

            self.create()

    def create(self) -> None:
        for (table, fields) in self.data.items():

            flist = []
            for f in fields:
                flist.append(f"{f['name']} {f['dtype']}")

            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table}(eid INTEGER PRIMARY KEY AUTOINCREMENT,{','.join(flist)})")
