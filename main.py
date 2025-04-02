import logging
import sqlite3

conn = None
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
DATA_BASE = "contoso-sales.db"

def connect() -> sqlite3.Connection:
    db_uri = f"{DATA_BASE}"
    try:
        conn = sqlite3.connect(db_uri, uri=True)
        logger.info("Connected to the database successfully")
        cursor = conn.cursor()
        # get_tables(cursor)
        get_records(cursor)    
        # get_schema(cursor)
        cursor.close()
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}")
    return conn

def get_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    logger.info("Tables in the database:")
    for row in cursor.fetchall():
        print(row[0])
    logger.info("Tables in the database fetched successfully")

def get_records(cursor):
    cursor.execute("SELECT * FROM sales_data")
    for row in cursor.fetchall():
        print(f"{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}, {row[7]}, {row[8]}, {row[9]}, {row[10]}")
        content = f"{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}, {row[7]}, {row[8]}, {row[9]}, {row[10]}"
        content = content + "\n"
        with open("sales_data.csv", "a") as f:
            f.write(content)
    logger.info("Data from the table fetched successfully")

def get_schema(cursor):
    schema = cursor.execute("PRAGMA table_info(sales_data);")
    logger.info("Schema of the table:")
    for row in schema.fetchall():
        content = (f"{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}")
        content = content + "\n"
        with open ("schema_data.csv", "a") as f:
            f.write(content)
    logger.info("Schema of the table fetched successfully")

def close(conn):
    conn.close()
    logger.info("Connection to the database closed successfully")

conn = connect()
close(conn)