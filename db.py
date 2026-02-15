import sqlite3
from uuid import uuid4


def init_db():
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()


    cursor.execute('''
                CREATE TABLE IF NOT EXISTS games (
                   id INTEGER PRIMARY KEY,
                   user_white_id INTEGER,
                   user_black_id INTEGER,
                   game_id TEXT,
                   won TEXT
                   )
            ''')
    conn.commit()
    conn.close()


def game_full(game_id):
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT user_white_id, user_black_id
                   FROM games
                   WHERE game_id = '{game_id}'
                   ''')
    users = cursor.fetchone()
    none_or_empty_count = sum(1 for users in users if users is None or users == '')
    conn.close()
    return none_or_empty_count == 0


def join_game(user_black_id, game_id):
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    cursor.execute(f'''
        UPDATE games
        SET user_black_id = {user_black_id}
        WHERE game_id = '{game_id}'
    ''')
    conn.commit()
    conn.close()


def get_user_id(game_id, color):
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT user_{color}_id
        FROM games
        WHERE game_id = '{game_id}'
    ''')
    user_id = cursor.fetchone()
    conn.close()
    return user_id


def create_game(user_white_id):
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    game_id = str(uuid4())
    cursor.execute(f'''
        INSERT INTO games (user_white_id, game_id)
        VALUES ({user_white_id}, '{game_id}')
    ''')
    conn.commit()
    conn.close()
    return game_id


def create_game_state_table():

    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS game_state  (
                   id INTEGER PRIMARY KEY,
                   game_id INTEGER,
                   next_black INTEGER,
                   game_state TEXT
        )
    ''')
    conn.commit()
    conn.close()