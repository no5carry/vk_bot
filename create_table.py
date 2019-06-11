import psycopg2
#создание таблицы пользователей с полями (уникальный id пользователя, чек-лист заданий, баланс пользовательских коинов)
try:
    conn = psycopg2.connect(dbname='vk_database', user='no5carry', password='pass2973')
except:
    print("I am unable to connect to the database")

cursor = conn.cursor()
try:
    cursor.execute("""
        CREATE TABLE users_date (
            user_id INT PRIMARY KEY,
            exercise_check VARCHAR(255),
            balance INT
        )
        """)
except:
    print("I can't drop our test database!")

conn.commit()
conn.close()
cursor.close()
