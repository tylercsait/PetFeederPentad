import mysql.connector
from mysql.connector import errorcode
from contextlib import contextmanager

"This code contains methods to use the DB"

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
    cursor = None
    try:
        connection = mysql.connector.connect(**config)
        print("Connection established")
        cursor = connection.cursor()
        yield cursor
        connection.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        close_connection(connection, cursor)

def __create_table(cursor, table_name, create_query):
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
    print(f"Finished dropping {table_name} table (if existed).")
    cursor.execute(create_query)
    print(f"Finished creating {table_name} table.")

def __get_column_value(cursor, table, column, rfid):
    query = f"SELECT {column} FROM {table} WHERE rfid = %s"
    cursor.execute(query, (rfid,))
    result = cursor.fetchone()
    return result[0] if result else None

def create_pets_table(cursor):
    create_query = """
    CREATE TABLE pets (
        rfid VARCHAR(50) PRIMARY KEY,
        rfid_text VARCHAR(50),
        max_feedings_day INTEGER,
        max_portions_day INTEGER,
        portions_per_feeding INTEGER
    );
    """
    __create_table(cursor, "pets", create_query)

def create_history_table(cursor):
    create_query = """
    CREATE TABLE history (
        rfid VARCHAR(50) PRIMARY KEY,
        date DATE,
        last_time_fed TIME,
        feedings_today INTEGER,
        portions_eaten_today INTEGER,
        leftover_portions INTEGER
    );
    """
    __create_table(cursor, "history", create_query)

def initialize_tables(cursor):
    create_pets_table(cursor)
    create_history_table(cursor)

def get_date_fed(cursor,rfid):
    return __get_column_value(cursor, "history", "date", rfid)

def get_last_time_fed(cursor, rfid):
    return __get_column_value(cursor, "history", "last_time_fed", rfid)

def get_feedings_today(cursor, rfid):
    return __get_column_value(cursor, "history", "feedings_today", rfid)

def get_portions_eaten_today(cursor, rfid):
    return __get_column_value(cursor, "history", "portions_eaten_today", rfid)

def get_leftover_portions(cursor, rfid):
    return __get_column_value(cursor, "history", "leftover_portions", rfid)

def get_rfid_text(cursor, rfid):
    return __get_column_value(cursor, "pets", "rfid_text", rfid)

def get_max_feedings_day(cursor, rfid):
    return __get_column_value(cursor, "pets", "max_feedings_day", rfid)

def get_max_portions_day(cursor, rfid):
    return __get_column_value(cursor, "pets", "max_portions_day", rfid)

def get_portion_per_feeding(cursor, rfid):
    return __get_column_value(cursor, "pets", "portions_per_feeding", rfid)


ALLOWED_TABLES = {'pets', 'history'}

def check_pet_exists(cursor, rfid, db):
    if db not in ALLOWED_TABLES:
        raise ValueError(f"Invalid table name: {db}")
    query = "SELECT 1 FROM {} WHERE rfid = %s".format(db)
    cursor.execute(query, (rfid,))
    return cursor.fetchone() is not None

def add_pet(cursor, rfid, rfid_text, max_feedings_day, max_portions_day, portions_per_feeding):
    insert_query = """
    INSERT INTO pets (rfid, rfid_text, max_feedings_day, max_portions_day, portions_per_feeding)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (rfid, rfid_text, max_feedings_day, max_portions_day, portions_per_feeding))
    print("Inserted", cursor.rowcount, "row(s) of data.")

    __init_history(cursor, rfid)

def add_history(cursor, rfid, last_time_fed, feedings_today, portions_eaten_today, leftover_portions):
    insert_query = """
        INSERT INTO history (rfid, date, last_time_fed, feedings_today, portions_eaten_today, leftover_portions)
        VALUES (%s, CURDATE(), %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (rfid, last_time_fed,feedings_today, portions_eaten_today, leftover_portions))
    print("Inserted", cursor.rowcount, "row(s) into history.")

def __init_history(cursor, rfid):
    add_history(cursor, rfid, -1, -1, -1, -1)

def update_pet_value(cursor, rfid, column, new_value):
    update_query = f"UPDATE pets SET {column} = %s WHERE rfid = %s"
    cursor.execute(update_query, (new_value, rfid))
    print(f"Updated {column} for", cursor.rowcount, "row(s).")

def update_pet_name(cursor, rfid, new_name):
    update_pet_value(cursor, rfid, "rfid_text", new_name)

def update_pet_portion_size(cursor, rfid, new_portion_size):
    update_pet_value(cursor, rfid, "portions_per_feeding", new_portion_size)

def update_pet_max_feedings(cursor, rfid, new_max_feedings):
    update_pet_value(cursor, rfid, "max_feedings_day", new_max_feedings)

def update_pet_feedings_today(cursor, rfid, new_feedings_today):
    update_pet_value(cursor, rfid, "max_portions_day", new_feedings_today)

def update_history_value(cursor, rfid, column, new_value):
    update_query = f"UPDATE history SET {column} = %s WHERE rfid = %s"
    cursor.execute(update_query, (new_value, rfid))
    print(f"Updated {column} for", cursor.rowcount, "row(s).")

def update_history_last_time_fed(cursor, rfid, new_last_fed):
    update_history_value(cursor, rfid, "last_time_fed", new_last_fed)

def update_history_feedings_today(cursor, rfid, new_feedings_today):
    update_history_value(cursor, rfid, "feedings_today", new_feedings_today)

def update_history_portions_eaten_today(cursor, rfid, new_portions_eaten_today):
    update_history_value(cursor, rfid, "portions_eaten_today", new_portions_eaten_today)

def update_history_leftover_portions(cursor, rfid, new_leftover_portions):
    update_history_value(cursor, rfid, "leftover_portions", new_leftover_portions)

def eligible_to_feed(cursor, rfid):
    if not check_pet_exists(cursor, rfid, "history"):
        return True  # No history implies pet can be fed
    max_meals = get_max_feedings_day(cursor, rfid) or 0
    meals_today = get_feedings_today(cursor, rfid) or 0
    return meals_today < max_meals


def list_all_pets(cursor):
    return view_table(cursor, "pets")

def view_table(cursor, db_name):
    query = f"SELECT * FROM {db_name}"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def delete_pet_by_rfid(cursor, rfid):
    delete_query = "DELETE FROM pets WHERE rfid = %s"
    cursor.execute(delete_query, (rfid,))
    print("Deleted", cursor.rowcount, "row(s).")
