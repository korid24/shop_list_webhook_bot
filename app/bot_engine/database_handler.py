import sqlite3


conn = sqlite3.connect('db.sqlite3', check_same_thread=False)
cursor = conn.cursor()


def user_is_exists(telegram_id: int) -> bool:
    """
    Проверяет, есть ли пользователь в бд
    """
    cursor.execute('SELECT * FROM users WHERE telegram_id=?', [(telegram_id)])
    if cursor.fetchall():
        return True
    return False


def get_user_position(telegram_id: int) -> int:
    """
    Получает текущую позицию пользователя
    """
    sql = 'SELECT * FROM users WHERE telegram_id=?'
    cursor.execute(sql, [(telegram_id)])
    return cursor.fetchall()[0][1]


def change_user_position(telegram_id: int, position: int) -> int:
    """
    Меняет текущую позицию пользователя
    """
    sql = 'UPDATE users SET position = ? WHERE telegram_id = ?'
    cursor.execute(sql, (position, telegram_id))
    conn.commit()
    return position


def create_user(telegram_id: int) -> bool:
    """
    Создаёт нового пользователя, если его не существует
    """
    if user_is_exists(telegram_id):
        change_user_position(telegram_id, 0)
        return False
    else:
        sql = 'INSERT INTO users VALUES (?,?)'
        cursor.execute(sql, (telegram_id, 0))
        conn.commit()
        return True
