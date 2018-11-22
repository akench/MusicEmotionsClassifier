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


def add_new_user(email, password):
    
    query = "INSERT INTO users VALUES('%s', '%s');" % (email, password)

    # get a connection from the pool and get a dictionary cursor
    conn = connection_pool.get_connection()
    cur = conn.cursor(dictionary=True)

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