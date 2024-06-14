import datetime
import sqlite3
from unittest import TestCase

import db


class TestDataBaseClass(TestCase):

    def test_conncetion(self):
        self.assertIsNotNone(db.get_connection())

    def test_init(self):
        db.init_db(force=True)
        with sqlite3.connect("calls.db") as conn:
            cursor = conn.execute("SELECT * from calls")
            columns = [desc[0] for desc in cursor.description]
            self.assertEqual(columns, ['id', 'user_id', 'date_created', 'date_expired'])

            cursor = conn.execute("SELECT * from phones")
            columns = [desc[0] for desc in cursor.description]
            self.assertEqual(columns, ['id', 'user_id', 'phone'])

    def test_add_call(self):
        db.init_db(force=True)
        date_created = datetime.datetime(2000, 1, 1, 2, 3, 4)
        date_expired = datetime.datetime(2000, 1, 1, 7, 3, 4)
        db.add_call(10, date_created, date_expired)

        with sqlite3.connect("calls.db") as conn:
            cursor = conn.execute("SELECT * from calls")
            n_rows = len(cursor.fetchall())
            self.assertEqual(n_rows, 1)

    def test_add_phone(self):
        db.init_db(force=True)
        db.add_phone(10, "+111111111111")

        with sqlite3.connect("calls.db") as conn:
            cursor = conn.execute("SELECT * from phones")
            n_rows = len(cursor.fetchall())
            self.assertEqual(n_rows, 1)

    def test_get_phone(self):
        db.init_db(force=True)
        db.add_phone(10, "+111111111111")
        phone = db.get_phone(10)
        self.assertEqual(phone, "+111111111111")

    def test_phone_to_call(self):
        db.init_db(force=True)

        date_created = datetime.datetime(2000, 1, 1, 2, 3, 4)
        date_expired = datetime.datetime(2000, 1, 1, 7, 3, 4)
        db.add_call(10, date_created, date_expired)
        db.add_phone(10, "+111111111111")

        curr_date = datetime.datetime(2000, 1, 1, 5, 3, 4)
        res = db.get_phones_to_call(curr_date)
        self.assertEqual(res, ["+111111111111"])
