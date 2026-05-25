import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",        
    "password": "",        
    "database": "aire_db"
}

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Errore connessione DB: {e}")
        return None

def execute_query(query, params=None, fetch=False):
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        if fetch:
            return cursor.fetchall()
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"Errore query: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
