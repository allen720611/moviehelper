import pymysql
uid=123
uname='ortonrocks'
config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'passwd': '!Qqaz2wsx',
        'db': 'try',
        'charset': 'utf8mb4',
        'local_infile': 1

    }

def insert_user_to_mysql(uid,uname):
    conn = pymysql.connect(**config)
    print('successfully connected')

    cur = conn.cursor()

    get_data_sql = "select * from user where uid = '"+str(uid)+"' ;"

    cur.execute(get_data_sql)
    data=cur.fetchall()
    if len(data)==0:
        insert_user_sql="insert into user (uid,uname) values ('{}','{}')".format(uid,uname)
        cur.execute(insert_user_sql)
        conn.commit()
        print('成功存入user資料')
    else:
        print('已經註冊過了！')
    cur.close()
    conn.close()



def insert_bookingdata_to_mysql(uname,mname,session):
    conn = pymysql.connect(**config)
    print('successfully connected')

    cur = conn.cursor()

    # get_data_sql = "select * from user where uid = '"+str(uid)+"' ;"
    #
    # cur.execute(get_data_sql)
    # data=cur.fetchall()
    # if len(data)==0:
    insert_user_sql="insert into movie_booking (uname, mname,session) values ('{}','{}','{}')".format(uname,mname,session)
    cur.execute(insert_user_sql)
    conn.commit()
    print('成功存入movie_booking資料')
    # else:
    # print('已經註冊過了！')
    cur.close()
    conn.close()



def insert_ratingdata_to_mysql(uname,mname,rate,comment):
    conn = pymysql.connect(**config)
    print('successfully connected')

    cur = conn.cursor()

    # get_data_sql = "select * from user where uid = '"+str(uid)+"' ;"
    #
    # cur.execute(get_data_sql)
    # data=cur.fetchall()
    # if len(data)==0:
    insert_user_sql="insert into movie_rating (uname, mname, rate,comment) values ('{}','{}','{}','{}')".format(uname,mname,rate,comment)
    cur.execute(insert_user_sql)
    conn.commit()
    print('成功存入movie_rating資料')
    # else:
    # print('已經註冊過了！')
    cur.close()
    conn.close()



