import sqlite3
import sys

from loguru import logger

from .configs.config import Config
from .exceptions import ContactNotFoundError, DuplicateContactError


class DbWorker:
    def __init__(self, config: Config):
        self.config = config
        self.connection = None
        self.cursor = None

    def init_db(self):
        try:
            self.connection = sqlite3.connect(self.config.db.db_name)
            self.cursor = self.connection.cursor()
        except Exception as e:
            logger.error(
                f"Failed to connect to data base {self.config.db.db_name}: {e.__class__.__name__}, {e}"
            )
            sys.exit("DB connection failed")
        exists = self.check_table_exists()
        if not exists:
            self.create_db()

    def check_table_exists(self) -> bool:
        try:
            self.cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (self.config.db.table_name,),
            )
            table_exists = self.cursor.fetchone() is not None
            return table_exists
        except Exception as e:
            logger.error(
                f"Failed to check table {self.config.db.table_name}: {e.__class__.__name__}, {e}"
            )
            raise e

    def create_db(self):
        try:
            self.cursor.execute(
                f"""
            CREATE TABLE IF NOT EXISTS {self.config.db.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                surname TEXT,
                phone_number TEXT,
                comment TEXT
              )
            """
            )
            self.connection.commit()
        except Exception as e:
            logger.error(
                f"Failed to create table {self.config.db.table_name}: {e.__class__.__name__}, {e}"
            )
            raise e

    def create_contact(self, name: str, surname: str, phone_number: str, comment: str):
        try:
            self.cursor.execute(
                f"INSERT INTO {self.config.db.table_name} (name, surname, phone_number, comment) VALUES (?, ?, ?, ?)",
                (name, surname, phone_number, comment),
            )
            self.connection.commit()
        except Exception as e:
            logger.error(f'Failed to save data for {name} {surname}: {e.__class__.__name__}, {e}')

    def get_all_contacts(self):
        try:
            self.cursor.execute('SELECT * FROM contacts')
            contacts = self.cursor.fetchall()
            return contacts
        except Exception as e:
            logger.error(f'Failed to get all contacts: {e.__class__.__name__}, {e}')
            return ""

    def find_contact(self, name: str, surname: str, exists: bool = True):
        self.cursor.execute('SELECT * FROM contacts WHERE name = ? AND surname = ?', (name, surname))
        contact = self.cursor.fetchone()
        if contact and not exists:
            logger.warning(f"Contact {name} {surname} already exists")
            raise DuplicateContactError(f'{name} {surname}')
        elif not contact and exists:
            logger.warning(f"Contact {name} {surname} wasn't found")
            raise ContactNotFoundError(f'{name} {surname}')
        return contact

    def update_contact(self, contact_id, name: str, surname: str, phone_number: str, comment: str):
        try:
            self.cursor.execute(
                'UPDATE contacts SET name=?, surname=?, phone_number=?, comment=? WHERE id=?',
                (name, surname, phone_number, comment, contact_id)
            )
            self.connection.commit()
        except Exception as e:
            logger.error(f'Failed to update contact for {name}, {surname}: {e.__class__.__name__}, {e}')

    def delete_contact(self, name: str, surname: str):
        try:
            self.cursor.execute('DELETE FROM contacts WHERE name=? AND surname=?', (name, surname))
            self.connection.commit()
        except Exception as e:
            logger.error(f'Failed to delete contact for {name} {surname}: {e.__class__.__name__}, {e}')

    def clear_contacts(self):
        try:
            self.cursor.execute('DELETE FROM contacts')
            self.connection.commit()
        except Exception as e:
            logger.error(f'Failed to clear contacts: {e.__class__.__name__}, {e}')

    def close_connection(self):
        self.connection.close()