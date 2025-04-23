import sqlite3

def run_sql_query(db_path, query):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(row)
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


