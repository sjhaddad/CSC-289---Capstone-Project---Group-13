import sqlite3


def create_table():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS users (
            first text,
            last text,
            total_income real,
            tax real
            )""")
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as e:
        print(f"Table creation failed: {e}")


def add_user(user):
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (:first, :last, :total_income, :tax)",
              (user.first, user.last, user.total_income, user.tax))
    conn.commit()
    conn.close()


def display_table():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE last = 'Palmer'")
    rows = c.fetchall()

    for row in rows:
        print(row)
    conn.close()
