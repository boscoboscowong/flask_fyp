import mysql.connector
from mysql.connector import Error


def execute_insert(query):
    """
    INSERT function in database
    No value would be returned
    """

    try:
        conn = mysql.connector.connect(user='root', password='', database='fyp')
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(query)
        conn.close()
        print('Connection closed')

    except Error as e:
        print(e)
        print("Cannot connect to database")



def execute_select(query):
    """
    SELECT query in database
    """

    try:
        conn = mysql.connector.connect(user='root', password='', database='fyp')
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows

    except Error as e:
        print(e)
        print('Cannot connect to database')



def execute_update(query):
    """
    UPDATE query in database
    """

    try:
        conn = mysql.connector.connect(user='root', password='', database='fyp')
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()

    except Error as e:
        print(e)
        print('Cannot connect to database')



def verify_user_login(query):

    try:
        conn = mysql.connector.connect(user='root', password='', database='fyp')
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchone()
        print rows
        conn.close()
        return rows

    except Error as e:
        print(e)
        print('Cannot connect to database')



