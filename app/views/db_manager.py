import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

try:
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="musicemotions_pool",
        pool_size=5,
        pool_reset_session=True,
        host='localhost',
        database='musicemotions',
        user='testuser',
        password='password'
    )
except Exception as e:
    print("exception in db")
    exit()


def get_password_for_user(email):

    conn = connection_pool.get_connection()
    cur = conn.cursor(dictionary=True)

    query = "SELECT * FROM users where email='%s';" % email
    password = None
    errno = 0
    try:
        cur.execute(query)
        row = cur.fetchone()

        # if the row is not null and its not 0 length
        if row and len(row):
            password = row['password']
    except mysql.connector.Error as err:
        print("login err: {}".format(err))
        errno = err.no
    finally:
        conn.close()

    return password, errno


def insert_user(email, password):
    

    # get a connection from the pool and get a dictionary cursor
    conn = connection_pool.get_connection()
    cur = conn.cursor(dictionary=True)

    query = "INSERT INTO users VALUES('%s', '%s');" % (email, password)
    try:
        cur.execute(query)
        conn.commit()
    except mysql.connector.IntegrityError as err:
        # if user already exists, 
        print("Error: {}".format(err))
        return err.errno
    finally:
        # whether we got an exception or not, close the connection
        conn.close()

    # no errors
    return 0