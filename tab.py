import psycopg2
import requests
from bs4 import BeautifulSoup

def insert_user(user_id, exercise_check, balance): # добавить пользователя в базу
    sql = """INSERT INTO users_date(user_id, exercise_check, balance)
             VALUES(%s, %s, %s);"""
    conn = None
    try:
        conn = psycopg2.connect(dbname='vk_database', user='no5carry', password='pass2973')
        cur = conn.cursor()
        cur.execute(sql, (user_id, exercise_check, balance,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_exercise(exercise_text, exercise_link, exercise_type, balance, price):#добавить задание в базу
    sql = """INSERT INTO exercise_date(exercise_text, exercise_link, exercise_type, balance, estimated_balance, price)
             VALUES(%s, %s, %s, %s, %s, %s);"""
    conn = None
    try:
        conn = psycopg2.connect(dbname='vk_database', user='no5carry', password='pass2973')
        cur = conn.cursor()
        cur.execute(sql, (exercise_text, exercise_link, exercise_type, balance, balance, price))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    update_users()

def update_user_other(user_id, exercise_check, balance):
    conn = None
    sql = """ UPDATE users_date
                SET exercise_check = %s,
                balance = %s
                WHERE user_id = %s"""
    try:
        conn = psycopg2.connect(dbname='vk_database', user='no5carry', password='pass2973')
        cur = conn.cursor()
        cur.execute(sql, (exercise_check,  balance, user_id))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_users():
    conn = None
    try:
        conn = psycopg2.connect(dbname='vk_database', user='no5carry', password='pass2973')
        cur = conn.cursor()
        cur.execute("SELECT user_id, exercise_check, balance  FROM users_date")
        print("All users: ", cur.rowcount)
        row = cur.fetchone()
        while row is not None:
            print(row)
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def check_users(user_id):
    conn = None
    check = False
    try:
        conn = psycopg2.connect(dbname='vk_database', user='no5carry', password='pass2973')
        cur = conn.cursor()
        cur.execute("SELECT user_id, exercise_check, balance  FROM users_date")
        row = cur.fetchone()
        while row is not None:
            if row[0] == user_id:
                check = True
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return check

def get_user_status(user_id):
    conn = None
    sql = "SELECT exercise_check, balance  FROM users_date WHERE user_id = %s;"
    try:
        conn = psycopg2.connect(dbname='vk_database', user='no5carry', password='pass2973')
        cur = conn.cursor()
        cur.execute(sql,([user_id]))
        row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return row[0][0]

def set_user_status(user_id,status):
    update_user(user_id,0,0,status)

def get_user_date(user_id):
    conn = None
    sql = "SELECT exercise_check, balance  FROM users_date WHERE user_id = %s;"
    try:
        conn = psycopg2.connect(dbname='vk_database', user='no5carry', password='pass2973')
        cur = conn.cursor()
        cur.execute(sql,([user_id]))
        row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return row

def get_num_list():# вернуть список заданий для нового пользователя
    conn = None
    num_list = 'z'
    try:
        conn = psycopg2.connect(dbname='vk_database', user='no5carry', password='pass2973')
        cur = conn.cursor()
        cur.execute("SELECT exercise_id, balance, estimated_balance  FROM exercise_date")
        row = cur.fetchone()
        while row is not None:
            if row[1] == 0:
                num_list += "4"
            elif row[2] == 0:
                num_list += "2"
            else:
                num_list += "0"
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return num_list

def update_user(user_id,num_exercise,plus_money,status):# обновления  юзера чек листа и добавление денег
    conn = None
    try:
        conn = psycopg2.connect(dbname='vk_database', user='no5carry', password='pass2973')
        cur = conn.cursor()
        sql = "SELECT user_id, exercise_check, balance  FROM users_date WHERE user_id = %s"
        cur.execute(sql, (user_id,))
        row = cur.fetchone()
        if row is not None:
            num_str = row[1]
            money = row[2]

        num_str = num_str[:num_exercise] + str(status) + num_str[num_exercise + 1:]
        sql2 = """ UPDATE users_date
                    SET exercise_check = %s,
                    balance = %s
                    WHERE user_id = %s"""
        cur.execute(sql2, (num_str,  plus_money + money, user_id))
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def update_user_money(user_id,plus_money):# обновления  юзера чек листа и добавление денег
    conn = None
    try:
        conn = psycopg2.connect(dbname='vk_database', user='no5carry', password='pass2973')
        cur = conn.cursor()
        sql = "SELECT user_id, exercise_check, balance  FROM users_date WHERE user_id = %s"
        cur.execute(sql, (user_id,))
        row = cur.fetchone()
        if row is not None:
            money = row[2]

        sql2 = """ UPDATE users_date
                    SET balance = %s
                    WHERE user_id = %s"""
        cur.execute(sql2, (plus_money + money, user_id))
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def update_user_money_minus(user_id,money_minus):# обновления  юзера чек листа и добавление денег
    conn = None
    try:
        conn = psycopg2.connect(dbname='vk_database', user='no5carry', password='pass2973')
        cur = conn.cursor()
        sql = "SELECT user_id, exercise_check, balance  FROM users_date WHERE user_id = %s"
        cur.execute(sql, (user_id,))
        row = cur.fetchone()
        if row is not None:
            money = row[2]

        sql2 = """ UPDATE users_date
                    SET balance = %s
                    WHERE user_id = %s"""
        cur.execute(sql2, (money-money_minus, user_id))
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def update_users():# обновляет статусы вопросов при добавлении нового вопроса
    conn = None
    try:
        conn = psycopg2.connect(dbname='vk_database', user='no5carry', password='pass2973')
        cur = conn.cursor()
        sql = "SELECT user_id, exercise_check FROM users_date"
        cur.execute(sql)
        status_list=[]
        row = cur.fetchone()
        while row is not None:
            status_list.append([row[0],row[1]+"0"])
            row = cur.fetchone()
        sql2 = """ UPDATE users_date
                    SET exercise_check = %s
                    WHERE user_id = %s"""
        for element in status_list:
            cur.execute(sql2, (element[1], element[0]))
            conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_exercise_for_execution(user_id,exercise_id):#взять задание на выполнение конкретному пользователю
    update_user(user_id,exercise_id, 0,"3")
    update_exercise_money(exercise_id,3)

def get_exercise(exercise_id):
    conn = None
    sql = "SELECT exercise_link, exercise_type, price, exercise_text  FROM exercise_date WHERE exercise_id = %s;"
    try:
        conn = psycopg2.connect(dbname='vk_database', user='no5carry', password='pass2973')
        cur = conn.cursor()
        cur.execute(sql,([exercise_id]))######################
        row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return row

def check_exercise(user_id,exercise_id,vk):
    if get_exercise(exercise_id)[1] == 0:
        return check_like_post(user_id,get_exercise(exercise_id)[0],vk)
    elif get_exercise(exercise_id)[1] == 1:
        return check_repost_on_wall(user_id,get_exercise(exercise_id)[0],vk)
    elif get_exercise(exercise_id)[1] == 2:
        return check_comment_post(user_id,get_exercise(exercise_id)[0],vk)
    elif get_exercise(exercise_id)[1] == 3:
        return check_member(user_id,get_exercise(exercise_id)[0],vk)
    elif get_exercise(exercise_id)[1] == 4:
        return check_follower(user_id,get_exercise(exercise_id)[0],vk)
    else:
        return False

def check_like_post(user_id,link,vk):
    link = link[link.find('wall')+4:]
    owner_id = link[:link.find('_')]
    item_id = link[link.find('_')+1:]
    like=vk.likes.isLiked(user_id=user_id,type='post',owner_id=owner_id,item_id=item_id)['liked']#user_id это тот,чей лайк мы проверяем,owner_id это страница человека на которой нужно поставить лайк
    if like==1:
        return True
    else:
        return False#проверка на лайк +++

def check_follower(user_id,link,vk_api):#проверка на подписку
    if "/club" in link:
        link = link[link.find('://vk.com')+14:]
    elif "/public" in link:
        link = link[link.find('://vk.com')+16:]
    else:
        link = link[link.find('://vk.com')+10:]
    check=vk_api.groups.isMember(group_id=link,user_id=user_id)
    if check:#проверяю,есть ли в этом числе айди человека,выполняющего задание
        return True
    else:
        return False

def check_repost_on_wall(user_id,link,vk_api):#проверка на репост +++
    link = link[link.find('wall')+4:]
    owner_id = link[:link.find('_')]
    item_id = link[link.find('_')+1:]
    reposts=vk_api.wall.get(type='post',owner_id=user_id,filter='other',count=20)['items']
    for repost in reposts:
        if 'copy_history' in repost:
            if (owner_id == str(repost['copy_history'][0]['owner_id']))and(str(repost['copy_history'][0]['id']) == item_id):
                return True
    return False

def check_comment_post(user_id,link,vk_api):#проверка на комментарий пд постом+++
    link = link[link.find('wall')+4:]
    owner_id = link[:link.find('_')]
    item_id = link[link.find('_')+1:]
    comments=vk_api.wall.getComments(owner_id=owner_id,post_id=item_id,count=100)['items']
    for comment in comments:
        if comment['from_id'] == user_id:
                return True
    return False

def check_member(user_id,link,vk_api):#проверка на подписку на группу
    if "/id" in link:
        link = link[link.find('://vk.com')+12:]
    else:
        link = link[link.find('://vk.com')+10:]
    owner_id=vk_api.users.get(user_ids=link)[0]['id']
    followers=vk_api.users.getFollowers(user_id=owner_id,count=1000)['items']#получаю последние 1000 подписавшихся людей на нужную страницу в количестве 1000
    print(followers)
    if user_id in followers:#проверяю,есть ли в этом числе айди человека,выполняющего задание
    #начисление коинов в бд
        return True
    else:
        return False

def update_exercise_money(exercise_id, status):
    conn = None
    try:
        conn = psycopg2.connect(dbname='vk_database', user='no5carry', password='pass2973')
        cur = conn.cursor()
        sql = "SELECT balance, estimated_balance, price  FROM exercise_date WHERE exercise_id = %s"
        cur.execute(sql, ([exercise_id]))#############################
        row = cur.fetchone()
        if status == 3:
            sql2 = """ UPDATE exercise_date
                        SET estimated_balance = %s
                        WHERE exercise_id = %s"""
            cur.execute(sql2, (row[1]-row[2],exercise_id))######################
            conn.commit()
            cur.close()
            if (row[1]-row[2] == 0):
                update_check_exercise_all_users(exercise_id,2)
        elif status == 1:
            sql2 = """ UPDATE exercise_date
                        SET balance = %s
                        WHERE exercise_id = %s"""
            cur.execute(sql2, (row[0]-row[2],exercise_id))################3
            conn.commit()
            cur.close()
            if (row[0]-row[2] == 0):
                update_check_exercise_all_users(exercise_id,4)
        elif status == 0:
            sql2 = """ UPDATE exercise_date
                        SET estimated_balance = %s
                        WHERE exercise_id = %s"""
            cur.execute(sql2, (row[1]+row[2],exercise_id))#################
            conn.commit()
            cur.close()
            if (row[1] == 0):
                update_check_exercise_all_users(exercise_id,0)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def exercise_completed(user_id,exercise_id):#обновить статус о задание на выполнено для заданого пользователя
    update_user(user_id,exercise_id, get_exercise(exercise_id)[2],"1")
    update_exercise_money(exercise_id,1)

def exercise_cancel(user_id,exercise_id):
    update_user(user_id,exercise_id, 0,"0")
    update_exercise_money(exercise_id,0)

def update_check_exercise_all_users(exercise_id,status): #обновить у всех юзерв статус задания на 0 или 2
    conn = None
    try:
        conn = psycopg2.connect(dbname='vk_database', user='no5carry', password='pass2973')
        cur = conn.cursor()
        sql = "SELECT user_id, exercise_check FROM users_date"
        cur.execute(sql)
        status_list=[]
        row = cur.fetchone()
        while row is not None:
            status_list.append([row[0],row[1]])
            row = cur.fetchone()
        sql2 = """ UPDATE users_date
                    SET exercise_check = %s
                    WHERE user_id = %s"""
        for element in status_list:
            if status == 2:
                if element[1][exercise_id] == "0":
                    element[1] = element[1][:exercise_id] + "2" +element[1][exercise_id+1:]
            elif status == 0:
                if element[1][exercise_id] == "2":
                    element[1] = element[1][:exercise_id] + "0" +element[1][exercise_id+1:]
            elif status == 4:
                element[1] = element[1][:exercise_id] + "4" +element[1][exercise_id+1:]
            cur.execute(sql2, (element[1], element[0]))
            conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
