import mysql.connector
from werkzeug.security import check_password_hash

# 连接到MySQL数据库
db = mysql.connector.connect(
    host='127.0.0.1',
    user='your_username',
    password='your_password',
    database='your_database'
)

def validate_user(username, password):
    cursor = db.cursor()
    query = "SELECT password FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    row = cursor.fetchone()

    if row is not None:
        hashed_password = row[0]
        if check_password_hash(hashed_password, password):
            return True

    return False