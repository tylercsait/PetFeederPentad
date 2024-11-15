import mysql.connector
from mysql.connector import errorcode
from contextlib import contextmanager

# Shared configuration for database connection
config = {
    'host': 'testsqlpentad.mysql.database.azure.com',
    'user': 'group3',
    'password': 'proj309@SAIT',
    'database': 'testdb'
    # 'client_flags': [mysql.connector.ClientFlag.SSL],
    # 'ssl_ca': '<path-to-SSL-cert>/DigiCertGlobalRootG2.crt.pem'
}

def close_connection(connection, cursor):
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    print("Connection closed.")

@contextmanager
def mysql_connection():
    connection = None
    db_cursor = None
    try:
        connection = mysql.connector.connect(**config)
        print("Connection established")
        db_cursor = connection.cursor()
        yield db_cursor
        connection.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        close_connection(connection, db_cursor)

def get_last_time_fed(cursor, rfid):
    query = "SELECT last_fed_time FROM pets WHERE RFID = %s"
    cursor.execute(query, (rfid,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_portion_size(cursor, rfid):
    query = "SELECT portion_size FROM pets WHERE RFID = %s"
    cursor.execute(query, (rfid,))
    result = cursor.fetchone()
    return result[0] if result else None

def check_pet_exists(cursor, rfid):
    query = "SELECT 1 FROM pets WHERE RFID = %s"
    cursor.execute(query, (rfid,))
    return cursor.fetchone() is not None

def add_pet(db_cursor, rfid, portions_today, max_portions, portion_size):
    insert_query = """
    INSERT INTO pets (RFID, portions_eaten_today, max_portions_day, portion_size)
    VALUES (%s, %s, %s, %s)
    """
    db_cursor.execute(insert_query, (rfid, portions_today, max_portions, portion_size))
    print("Inserted", db_cursor.rowcount, "row(s) of data.")

def update_pet_portion_size(db_cursor, rfid, new_portion_size):
    update_query = "UPDATE pets SET portion_size = %s WHERE RFID = %s"
    db_cursor.execute(update_query, (new_portion_size, rfid))
    print("Updated portion size for", db_cursor.rowcount, "row(s).")

def update_pet_max_feedings(db_cursor, rfid, new_max_feedings):
    update_query = "UPDATE pets SET max_portions_day = %s WHERE RFID = %s"
    db_cursor.execute(update_query, (new_max_feedings, rfid))
    print("Updated max feedings for", db_cursor.rowcount, "row(s).")

def update_pet_feedings_today(db_cursor, rfid, new_feedings_today):
    update_query = "UPDATE pets SET portions_eaten_today = %s WHERE RFID = %s"
    db_cursor.execute(update_query, (new_feedings_today, rfid))
    print("Updated feedings today for", db_cursor.rowcount, "row(s).")

def list_all_pets(db_cursor):
    query = "SELECT * FROM pets"
    db_cursor.execute(query)
    rows = db_cursor.fetchall()
    return rows

def view_data(cursor):
    cursor.execute("SELECT * FROM pets")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def delete_pet_by_rfid(db_cursor, rfid):
    delete_query = "DELETE FROM pets WHERE RFID = %s"
    db_cursor.execute(delete_query, (rfid,))
    print("Deleted", db_cursor.rowcount, "row(s).")
