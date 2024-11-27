import mysql.connector
from datetime import datetime, date, timedelta
import json

# 从配置文件中读取数据库连接信息
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

DB_HOST = config['DB_HOST']
DB_USER = config['DB_USER']
DB_PASSWORD = config['DB_PASSWORD']
DB_NAME = config['DB_NAME']

def mysql_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

TODAY = date.today()

def init_history_today(cursor, rfid):
    # 检查今天是否已有历史记录，如果没有则插入一条新的
    query = "SELECT COUNT(*) FROM history WHERE rfid = %s AND date = %s"
    cursor.execute(query, (rfid, TODAY))
    count = cursor.fetchone()[0]
    print(f"History records for RFID {rfid} on {TODAY}: {count}")  # 调试信息
    if count == 0:
        insert_query = "INSERT INTO history (rfid, date, feedings_today, portions_eaten_today, leftover_portions) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (rfid, TODAY, 0, 0, 0))
        print(f"Inserted new history record for RFID {rfid} on {TODAY}")
    else:
        print(f"History record already exists for RFID {rfid} on {TODAY}")

def get_feedings_today(cursor, rfid):
    value = get_column_value_for_date(cursor, "history", "feedings_today", rfid, TODAY)
    print(f"Retrieved feedings_today from database: {value}")  # 调试信息
    return value

def get_column_value_for_date(cursor, table, column, rfid, date_value):
    query = f"SELECT {column} FROM {table} WHERE rfid = %s AND date = %s"
    cursor.execute(query, (rfid, date_value))
    result = cursor.fetchone()
    if result:
        value = result[0]
        print(f"Value retrieved for {column}: {value}")  # 调试信息
        return value
    else:
        print(f"No value found for {column} on date {date_value} for RFID {rfid}")  # 调试信息
        return None

def update_history_feedings_today(cursor, rfid, new_feedings_today):
    print(f"Updating feedings_today to {new_feedings_today} for RFID {rfid}")  # 调试信息
    update_history_value(cursor, rfid, TODAY, "feedings_today", new_feedings_today)

def update_history_value(cursor, rfid, the_date, column, new_value):
    print(f"Updating {column} to {new_value} for RFID {rfid} on date {the_date}")  # 调试信息
    update_query = f"UPDATE history SET {column} = %s WHERE rfid = %s AND date = %s"
    cursor.execute(update_query, (new_value, rfid, the_date))
    print(f"Updated {column} for {cursor.rowcount} row(s).")  # 调试信息

def increment_feeding_history(cursor, rfid):
    # 确保今天的历史记录存在
    init_history_today(cursor, rfid)
    
    # 获取当前的 feedings_today 值
    feedings = get_feedings_today(cursor, rfid)
    print(f"Current feedings_today: {feedings}")  # 调试信息

    # 确保 feedings 是数值类型
    try:
        if feedings is None:
            feedings = 0
        else:
            feedings = int(feedings)
    except ValueError:
        print(f"Invalid feedings_today value: {feedings}. Setting to 0.")
        feedings = 0

    # 增加 feedings_today 的计数
    new_feedings = feedings + 1
    print(f"Incremented feedings_today: {new_feedings}")  # 调试信息
    update_history_feedings_today(cursor, rfid, new_feedings)

    # 更新 last_time_fed
    update_history_last_time_fed(cursor, rfid, datetime.now())

def update_history_last_time_fed(cursor, rfid, new_last_time_fed):
    print(f"Updating last_time_fed to {new_last_time_fed} for RFID {rfid}")  # 调试信息
    update_query = "UPDATE history SET last_time_fed = %s WHERE rfid = %s AND date = %s"
    cursor.execute(update_query, (new_last_time_fed, rfid, TODAY))
    print(f"Updated last_time_fed for {cursor.rowcount} row(s).")  # 调试信息

def eligible_to_feed(cursor, rfid):
    try:
        # 获取宠物的上次喂食时间
        query = "SELECT last_time_fed FROM history WHERE rfid = %s ORDER BY date DESC LIMIT 1"
        cursor.execute(query, (rfid,))
        result = cursor.fetchone()

        if result and result[0]:
            last_time_fed = result[0]
        #     定义允许再次喂食的最小间隔时间
        #     feeding_interval = timedelta(hours=2)  # 根据您的需求调整
        #     next_allowed_time = last_time_fed + feeding_interval
        #     now = datetime.now()
        #     if now >= next_allowed_time:
        #         return True
        #     else:
        #         return False
            return True
        else:
        #    如果没有喂食记录，允许喂食
            return True
    except mysql.connector.Error as err:
        print(f"Database error in eligible_to_feed: {err}")
        return False

def get_portion_per_feeding(cursor, rfid):
    try:
        # 从数据库中获取每次喂食的份数
        query = "SELECT portions_per_feeding FROM pets WHERE rfid = %s"
        cursor.execute(query, (rfid,))
        result = cursor.fetchone()
        if result and result[0]:
            portions_per_feeding = result[0]
            print(f"Portion per feeding for RFID {rfid}: {portions_per_feeding}")  # 调试信息
            return portions_per_feeding
        else:
            print(f"No portions_per_feeding found for RFID {rfid}. Using default value 1.")
            return 1  # 默认值
    except mysql.connector.Error as err:
        print(f"Database error in get_portion_per_feeding: {err}")
        return 1  # 默认值

def increment_portions_eaten_history(cursor, rfid, portions_eaten):
    # 确保今天的历史记录存在
    init_history_today(cursor, rfid)
    
    # 获取当前的 portions_eaten_today 值
    portions_eaten_today = get_portions_eaten_today(cursor, rfid)
    print(f"Current portions_eaten_today: {portions_eaten_today}")  # 调试信息

    # 确保 portions_eaten_today 是数值类型
    try:
        if portions_eaten_today is None:
            portions_eaten_today = 0.0
        else:
            portions_eaten_today = float(portions_eaten_today)
    except ValueError:
        print(f"Invalid portions_eaten_today value: {portions_eaten_today}. Setting to 0.")
        portions_eaten_today = 0.0

    # 增加 portions_eaten_today
    new_portions_eaten_today = portions_eaten_today + portions_eaten
    print(f"Incremented portions_eaten_today: {new_portions_eaten_today}")  # 调试信息
    update_history_portions_eaten_today(cursor, rfid, new_portions_eaten_today)

def get_portions_eaten_today(cursor, rfid):
    value = get_column_value_for_date(cursor, "history", "portions_eaten_today", rfid, TODAY)
    print(f"Retrieved portions_eaten_today from database: {value}")  # 调试信息
    return value

def update_history_portions_eaten_today(cursor, rfid, new_portions_eaten_today):
    print(f"Updating portions_eaten_today to {new_portions_eaten_today} for RFID {rfid}")  # 调试信息
    update_history_value(cursor, rfid, TODAY, "portions_eaten_today", new_portions_eaten_today)

# 示例用法
if __name__ == "__main__":
    try:
        connection = mysql_connection()
        cursor = connection.cursor()
        rfid = '302833627647'  # 示例 RFID
        increment_feeding_history(cursor, rfid)
        connection.commit()
        print("Database update committed.")
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        cursor.close()
        connection.close()
