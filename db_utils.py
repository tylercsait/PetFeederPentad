from datetime import datetime, date
import mysql.connector
from mysql.connector import errorcode
from contextlib import contextmanager

"This code contains methods to use the DB"

TODAY = date.today()
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
        cursor = connection.cursor(buffered=True)  # Use a buffered cursor
        yield cursor, connection
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

def get_column_value_for_date(cursor, table, column, rfid, date):
    query = f"SELECT {column} FROM {table} WHERE rfid = %s AND date = %s"
    cursor.execute(query, (rfid, date))
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
        rfid VARCHAR(50),
        date DATE,
        last_time_fed TIME NULL,
        feedings_today INTEGER,
        portions_eaten_today INTEGER,
        leftover_portions INTEGER,
        PRIMARY KEY (rfid, date)  -- Composite primary key
    );
    """
    __create_table(cursor, "history", create_query)

def initialize_tables(cursor):
    create_pets_table(cursor)
    create_history_table(cursor)

def get_date_fed(cursor,rfid, the_date):
    return get_column_value_for_date(cursor, "history", "date", rfid, the_date)

def get_last_time_fed(cursor, rfid, the_date):
    return get_column_value_for_date(cursor, "history", "last_time_fed", rfid, the_date)

def get_feedings_today(cursor, rfid):
    return get_column_value_for_date(cursor, "history", "feedings_today", rfid, TODAY)

def get_portions_eaten(cursor, rfid, the_date):
    return get_column_value_for_date(cursor, "history", "portions_eaten_today", rfid, the_date)

def get_leftover_portions(cursor, rfid, the_date):
    return get_column_value_for_date(cursor, "history", "leftover_portions", rfid, the_date)

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

def add_history(cursor, rfid, the_date, last_time_fed, feedings_today, portions_eaten_today, leftover_portions):
    insert_query = """
        INSERT INTO history (rfid, date, last_time_fed, feedings_today, portions_eaten_today, leftover_portions)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (rfid, the_date, last_time_fed, feedings_today, portions_eaten_today, leftover_portions))
    print("Inserted", cursor.rowcount, "row(s) into history.")

def __init_history(cursor, rfid):
    add_history(cursor, rfid, TODAY, None, 0, 0, 0)

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

def update_history_value(cursor, rfid, the_date, column, new_value):
    update_query = f"UPDATE history SET {column} = %s WHERE rfid = %s AND date = %s"
    cursor.execute(update_query, (new_value, rfid, the_date))
    print(f"Updated {column} for", cursor.rowcount, "row(s).")

def update_history_last_time_fed(cursor, rfid, new_last_fed):
    update_history_value(cursor, rfid, TODAY,"last_time_fed", new_last_fed)

def update_history_feedings_today(cursor, rfid, new_feedings_today):
    update_history_value(cursor, rfid, TODAY, "feedings_today", new_feedings_today)

def update_history_portions_eaten_today(cursor, rfid, new_portions_eaten_today):
    update_history_value(cursor, rfid, TODAY, "portions_eaten_today", new_portions_eaten_today)

def update_history_leftover_portions(cursor, rfid, the_date, new_leftover_portions):
    update_history_value(cursor, rfid, the_date, "leftover_portions", new_leftover_portions)

def eligible_to_feed(cursor, rfid):
    if not check_pet_exists(cursor, rfid, "history"):
        return True  # No history implies pet can be fed
    max_meals = get_max_feedings_day(cursor, rfid) or 0
    meals_today = get_feedings_today(cursor, rfid) or 0
    return meals_today < max_meals


def increment_feeding_history(cursor, rfid):
    # Check if the record for TODAY exists
    if get_date_fed(cursor, rfid, TODAY) is None:
        # Insert a new record for today
        add_history(cursor, rfid, TODAY,None, 0, 0, 0)

    # Safely handle None values by defaulting to 0
    feedings = get_feedings_today(cursor, rfid) or 0

    # Increment feedings count
    update_history_feedings_today(cursor, rfid, feedings + 1)
    # Update the last time fed to the current time
    update_history_last_time_fed(cursor, rfid, datetime.now().time())


def increment_portions_eaten_history(cursor, rfid, portions_eaten):
    portions = get_portions_eaten(cursor, rfid, TODAY)
    update_history_portions_eaten_today(cursor, rfid, portions+portions_eaten)

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
    cursor.execute(delete_query, ( rfid,))
    print("Deleted", cursor.rowcount, "row(s) from pets.")
    delete_query = "DELETE FROM history WHERE rfid = %s"
    cursor.execute(delete_query, (rfid,))
    print("Deleted", cursor.rowcount, "row(s) from history.")


def create_file_name(cursor, rfid):
    # Fetch the required data from the database
    cursor.execute(
        "SELECT date, last_time_fed FROM history WHERE rfid = %s ORDER BY date DESC, last_time_fed DESC LIMIT 1",
        (rfid,))
    row = cursor.fetchone()

    if row:
        date = row[0].strftime('%Y-%m-%d')  # Format date as YYYY-MM-DD
        # last_time_fed = row[1].strftime('%H-%M-%S')  # Format time as HH-MM-SS
        file_name = f"{rfid}-{date}.jpg"
    else:
        file_name = f"{rfid}-no-data.jpeg"

    return file_name

