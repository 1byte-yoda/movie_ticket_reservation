"""Don't forget to add the sql_mode configuration in ubuntu"""

import pymysql

connection = pymysql.connect(host='',
                             user='',
                             password='',
                             db='',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

for _ in range(1, 201):
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `seat` (`screen_id`) VALUES (%s)"
        cursor.execute(sql, (2, ))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()


try:
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM `seat`"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
finally:
    connection.close()
