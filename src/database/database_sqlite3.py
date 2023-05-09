import sqlite3
from dataclasses import dataclass


@dataclass
class DatabaseHelper:
    db_name: str = "driver.db"


class Driver:
    def __init__(self, name: str, surname: str, gender: str, age: int, tc: int, plate: str):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.age = age
        self.tc = tc
        self.plate = plate

    def save(self):
        conn = sqlite3.connect(DatabaseHelper.db_name)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS drivers(name TEXT, surname TEXT, gender TEXT, age INTEGER, tc INTEGER, plate TEXT)')
        cursor.execute('INSERT INTO drivers VALUES (?, ?, ?, ?, ?, ?)',
                       (self.name, self.surname, self.gender, self.age, self.tc, self.plate))
        conn.commit()
        conn.close()

    @classmethod
    def delete(cls, tc: int):
        conn = sqlite3.connect(DatabaseHelper.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM drivers WHERE tc = ?', (tc,))
        conn.commit()
        conn.close()

    @classmethod
    def update(cls, tc: int, name: str, surname: str, gender: str, age: int, plate: str):
        conn = sqlite3.connect(DatabaseHelper.db_name)
        cursor = conn.cursor()
        cursor.execute('UPDATE drivers SET name = ?, surname = ?, gender = ?, age = ?, plate = ? WHERE tc = ?',
                       (name, surname, gender, age, plate, tc))
        conn.commit()
        conn.close()

    @classmethod
    def get_all(cls):
        conn = sqlite3.connect(DatabaseHelper.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM drivers')
        rows = cursor.fetchall()
        drivers = []
        for row in rows:
            driver = Driver(row[0], row[1], row[2], row[3], row[4], row[5])
            drivers.append(driver)
        conn.close()
        return drivers

    @classmethod
    def get_by_plate(cls, plate:str):
        conn = sqlite3.connect(DatabaseHelper.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM drivers WHERE plate = ?', (plate,))
        row = cursor.fetchone()
        if row is None:
            return None
        driver = Driver(row[0], row[1], row[2], row[3], row[4], row[5])
        conn.close()
        return driver
