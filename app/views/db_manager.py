import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

try:
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="musicemotions_pool",
        pool_size=5,
        pool_reset_session=False,
        host='localhost',
        database='musicemotions',
        user='testuser',
        password='password'
    )
except Exception as e:
    print("exception in db")
    exit()


def get_password_for_user(email):
    '''
    Queries the database to get the password for a given user

    Args:
        email (str): user to get password for

    Returns:
        password (str)
        errno (int) : error code if gave error
    '''

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
        print("returning to pool get password")
        conn.close()

    return password, errno


def insert_user(email, password):
    '''
    insert new user into database

    Args:
        email (str)
        password (str)

    Returns:
        errno (int) : error code if was error
    '''
    
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
        print('returning to pool register')
        conn.close()

    # no errors
    return 0


def get_songs_for_user(email):
    '''
    Gets all of the songs for a specified user

    Args:
        email (str): user to get songs of

    Returns:
        list of dictionaries : containing the rows
        int : errno
    '''
    # get connection and cursor
    conn = connection_pool.get_connection()
    cur = conn.cursor(dictionary=True)

    query = "SELECT songemotions.* FROM usersongs INNER JOIN songemotions ON usersongs.songurl=songemotions.songurl WHERE email='%s';" % email
    
    songs = []
    errno = 0
    try:
        cur.execute(query)
        songs = cur.fetchall()
    except Error as err:
        print("Error: {}".format(err))
        errno = err.errno
    finally:
        # return connection to pool
        print('return to pool get songs')
        conn.close()

    return songs, errno


def insert_song(url, title, emot):
    # get connection
    conn = connection_pool.get_connection()
    cur = conn.cursor(dictionary=True)

    query = "INSERT INTO songemotions VALUES('%s', '%s', '%s');" % (url, title, emot)
    
    try:
        cur.execute(query)
        conn.commit()
    except mysql.connector.IntegrityError as err:
        # if we get an integrity error, means that song is already in the table
        # so don't do anything
        print("error inserting song: ", err.args)
    finally:
        conn.close()
    
def insert_user_song(email, url):
    # get connection
    conn = connection_pool.get_connection()
    cur = conn.cursor(dictionary=True)

    query = "INSERT INTO usersongs VALUES('%s', '%s');" % (email, url)

    try:
        cur.execute(query)
        conn.commit()
    except mysql.connector.IntegrityError as err:
        # user has already added this song
        print("error adding song to user", err.args)
    finally:
        conn.close()


def is_song_in_db(url):

    # get connection
    conn = connection_pool.get_connection()
    cur = conn.cursor(dictionary=True)

    query = "SELECT * FROM songemotions where songurl='%s';" % url

    try:
        cur.execute(query)
        song = cur.fetchall()

        return len(song) > 0
    except Error as err:
        print("Error : {}".format(err))
        return False
    finally:
        conn.close()

