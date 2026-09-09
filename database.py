import sqlite3
import json

def create_database():
    with sqlite3.connect("main.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Аккаунты (
                Логин VARCHAR(20) PRIMARY KEY,
                Пароль VARCHAR(20) )
        ''')
        conn.commit()

def auth(username, password):
    with sqlite3.connect("main.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Аккаунты WHERE Логин = ? AND Пароль = ?", (username,password))
        data = cursor.fetchall()
        if(data):
            return True
        else:
            return False
        
def change_password(username, old_password, new_password):
    with sqlite3.connect("main.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Аккаунты WHERE Логин = ? AND Пароль = ?", (username,old_password))
        data = cursor.fetchall()
        if(data):
            cursor.execute("UPDATE Аккаунты SET Пароль = ? WHERE Логин = ?", (new_password, username))
            conn.commit()
            return True
        else:
            return False
        
def get_homeworks(username):
    with sqlite3.connect("main.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT Домашние_задания FROM Аккаунты WHERE Логин = ?",
            (username,)
        )
        data = cursor.fetchone()
        if data and data[0]:
            return json.loads(data[0])
        return []


def add_homework(username, title, description, image):
    with sqlite3.connect("main.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT Домашние_задания FROM Аккаунты WHERE Логин = ?",
            (username,)
        )
        data = cursor.fetchone()
        if not data:
            return False
        if data[0]:
            homeworks = json.loads(data[0])
        else:
            homeworks = []
            
        new_homework = {
            "name": title,
            "description": description,
            "image": image
        }
        homeworks.append(new_homework)
        homeworks_json = json.dumps(homeworks, ensure_ascii=False)

        cursor.execute(
            """
            UPDATE Аккаунты
            SET Домашние_задания = ?
            WHERE Логин = ?
            """,
            (homeworks_json, username)
        )
        conn.commit()
        return homeworks


create_database()
