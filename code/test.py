import pymysql

connection = pymysql.connect(host="localhost", user="root", password="123456",
                             db="anonymouse", charset="utf8mb4",
                             cursorclass=pymysql.cursors.DictCursor)


def create_account():
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO account (`email`, `password`) VALUES (%s, %s);"
            cursor.execute(sql, ("mastermind@anonymouse.com", "123456"))

        connection.commit()

        with connection.cursor() as cursor:
            sql = "SELECT * FROM account;"
            cursor.execute(sql)
            result = cursor.fetchall()

        for account in result:
            print(account)
    finally:
        connection.close()
