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


def update_user(user):
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("UPDATE users SET total_income = :total_income, tax = :tax WHERE first = :first AND last = :last",
              {'first': user.first, 'last': user.last, 'total_income': user.total_income, 'tax': user.tax})
    conn.commit()
    conn.close()


def display_table():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    rows = c.fetchall()

    for row in rows:
        print(row)
    conn.close()


def display_user_info_by_name(first_name, last_name):
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE first = :first AND last = :last",
              {'first': first_name, 'last': last_name})
    result = c.fetchone()
    conn.close()

    if result:
        print(f"User Information: {result}")
    else:
        print(f"No user found with the name {first_name} {last_name}")
