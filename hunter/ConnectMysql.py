
import pymysql.cursors
# Connect to the database

connection=None

def ConnectMysql(db):
    global  connection
    connection = pymysql.connect(host='127.0.0.1',

                                 port=3306,

                                 user='root',

                                 password='111',

                                 db=db,

                                 charset='utf8mb4',

                                 cursorclass=pymysql.cursors.DictCursor)
    print("CONNECT OK")



# Select Data

def SelectData(Sqlstring):
    try:
        with connection.cursor() as cursor:
            cursor.execute(Sqlstring)       # 执行sql语句
            result = cursor.fetchall()
            for re in result:              #re为字典对象
                print(re)
        connection.commit()

    finally:
        print("remenber to Close Connection")
        connection.close()
    return result
