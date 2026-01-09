import sqlite3

DB_NAME = "database.db"

def init():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_user (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255) UNIQUE,
            password VARCHAR(255)
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_games (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255),
            players INTEGER,
            quantity INTEGER,
            rented_by VARCHAR(255)
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_rented (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            quantity INTEGER
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_food (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255),
            quantity INTEGER
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_profile (
            id INTEGER PRIMARY KEY,
            email VARCHAR(255),
            game VARCHAR(255),
            food VARCHAR(255),
            quantity_food INTEGER
        );
    """)
    conn.commit()
    conn.close()

def initial_stock():
    games = [
        ("Arkham", 4, 1),
        ("Trivial Pursuit", 6, 1),
        ("Madness", 5, 1),
        ("Nosferatu", 8, 1),
        ("Eldritch", 8, 1),
        ("Halloween", 4, 1),
        ("Dreadful Circus", 8, 1)
    ]

    foods = [
        ("Mumias sichas", 10),
        ("Cento-salgado", 10),
        ("Cupcake witch", 10),
        ("Milkshake de abobora", 10),
        ("Caolho", 10)
    ]
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tbl_games;")
    count_games = cursor.fetchone()[0]
    if count_games == 0:
        cursor.executemany(
            "INSERT INTO tbl_games (name, players, quantity, rented_by) VALUES (?, ?, ?, NULL)",
            games
        )
    cursor.execute("SELECT COUNT(*) FROM tbl_food;")
    count_foods = cursor.fetchone()[0]
    if count_foods == 0:
        cursor.executemany(
            "INSERT INTO tbl_food (name, quantity) VALUES (?, ?)",
            foods
        )
    conn.commit()
    conn.close()

def insert_user(name, email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tbl_user (name, email, password) VALUES (?, ?, ?);",
        (name, email, password)
    )
    conn.commit()
    conn.close()

def check_login(email, password):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM tbl_user WHERE email = ? AND password = ?;",
        (email, password)
    )
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    return dict(row)

def read_user(email):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_user WHERE email = ?;", (email,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    return dict(row)

def delete_user_by_email(email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tbl_user WHERE email = ?;", (email,))
    conn.commit()
    conn.close()

def update_user_password(email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tbl_user SET password = ? WHERE email = ?;",
        (password, email)
    )
    conn.commit()
    conn.close()

def insert_game(name, players, quantity):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tbl_games (name, players, quantity, rented_by) VALUES (?, ?, ?, NULL);",
        (name, players, quantity)
    )
    conn.commit()
    conn.close()

def read_game(name):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_games WHERE name = ?;", (name,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    return dict(row)

def delete_game_by_name(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tbl_games WHERE name = ?;", (name,))
    conn.commit()
    conn.close()

def update_game_quantity(name, quantity):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tbl_games SET quantity = ? WHERE name = ?;",
        (quantity, name)
    )
    conn.commit()
    conn.close()

def update_game_rented_by(name, email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tbl_games
        SET rented_by = ?
        WHERE name = ? AND rented_by IS NULL;
    """, (email, name))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected

def clear_game_rented_by(email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tbl_games
        SET rented_by = NULL
        WHERE rented_by = ?;
    """, (email,))
    conn.commit()
    conn.close()

def check_game_rented(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT rented_by
        FROM tbl_games
        WHERE name = ? AND rented_by IS NOT NULL;
    """, (name,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def get_rented_game(email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM tbl_games WHERE rented_by = ?;",
        (email,)
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def clear_game_rented_by_user(email, game):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tbl_games
        SET rented_by = NULL
        WHERE rented_by = ? AND name = ?;
    """, (email, game))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0

def check_game_rented_by_user(user_email):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name
        FROM tbl_games
        WHERE rented_by = ?;
    """, (user_email,))
    row = cursor.fetchone()
    conn.close()
    return row["name"] if row else None

def insert_rented(name, email, quantity):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tbl_rented (name, email, quantity) VALUES (?, ?, ?);",(name, email, quantity))
    conn.commit()
    conn.close()

def read_rented(email):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_rented WHERE email = ?;", (email,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    return dict(row)

def delete_rented_by_email(email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tbl_rented WHERE email = ?;", (email,))
    conn.commit()
    conn.close()

def update_rented_quantity(email, quantity):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE tbl_rented SET quantity = ? WHERE email = ?;", (quantity, email))
    conn.commit()
    conn.close()

def insert_food(name, quantity):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tbl_food (name, quantity) VALUES (?, ?);", (name, quantity))
    conn.commit()
    conn.close()

def read_food(name):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_food WHERE name = ?;", (name,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    return dict(row)

def delete_food_by_name(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tbl_food WHERE name = ?;", (name,))
    conn.commit()
    conn.close()

def update_food_quantity(name, quantity):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE tbl_food SET quantity = ? WHERE name = ?;", (quantity, name))
    conn.commit()
    conn.close()

def insert_profile(email, game, food, quantity_food):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tbl_profile (email, game, food, quantity_food) VALUES (?, ?, ?, ?);", (email, game, food, quantity_food))
    conn.commit()
    conn.close()

def read_profile(email):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_profile WHERE email = ?;", (email,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    return dict(row)

def delete_profile_by_email(email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tbl_profile WHERE email = ?;", (email,))
    conn.commit()
    conn.close()

def update_profile_game(email, game):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE tbl_profile SET game = ? WHERE email = ?;", (game, email))
    conn.commit()
    conn.close()

def update_profile_food(email, food):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE tbl_profile SET food = ? WHERE email = ?;",(food, email))
    conn.commit()
    conn.close()

def update_profile_food_quantity(email, quantity_food):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE tbl_profile SET quantity_food = ? WHERE email = ?;", (quantity_food, email))
    conn.commit()
    conn.close()

def add_rented_by_column():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE tbl_games ADD COLUMN rented_by VARCHAR(255);")
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f"Info: coluna rented_by já existe ou erro ao adicionar: {e}")
    conn.close()