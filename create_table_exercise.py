import psycopg2
#создание таблицы заданий с полями (уникальный id задания; текст задания; ссылка на задние; тип задания: группа, страница юзера, пост; тип события: лайк, репост, подписка; баланс;оценочный баланс; прайс)
try:
    conn = psycopg2.connect(dbname='vk_database', user='no5carry', password='pass2973')
except:
    print("I am unable to connect to the database")

cursor = conn.cursor()
try:
    cursor.execute("""
        CREATE TABLE exercise_date (
            exercise_id serial PRIMARY KEY,
            exercise_text TEXT,
            exercise_link TEXT,
            exercise_type INT,
            balance INT,
            estimated_balance INT,
            price INT
        )
        """)
except:
    print("I can't drop our test database!")

conn.commit()
conn.close()
cursor.close()
