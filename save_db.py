import sqlite3

db = sqlite3.connect('users.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    user_name VARCHAR,
    first_name VARCHAR,
    last_name VARCHAR,
    user_request TEXT
)""")
db.commit()


def save_user_answer(user_id, user_name, first_name, last_name, user_request):
    with sqlite3.connect('users.db') as conn:
        sql = conn.cursor()
        sql.execute("\
            INSERT INTO users (user_id, user_name, first_name, last_name, user_request) \
            VALUES (?,?,?,?,?);", 
            (user_id, user_name, first_name, last_name, user_request,))
        conn.commit()
