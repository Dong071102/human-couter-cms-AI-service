import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import psycopg2
from config.db_config import DB_HOST, PORT, DB_DATABASE, DB_USER, DB_PASSWORD
def get_connection():
    conn=psycopg2.connect(
        host=DB_HOST,
        port=PORT,
        dbname=DB_DATABASE,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

def get_all_camera_ip():
    query="""
        select camera_id,camera_URL, classroom_id, socket_path
        from cameras 
        where camera_type='surveillance'"""
    try:
        conn=get_connection()
        cur=conn.cursor()

        cur.execute(query)
        row=cur.fetchall()
        return row
    except Exception as e:
        print(f"Error when get camra ip:{e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def insert_snapshot_person(schedule_id,camera_id,people_couter,captured_at,image_path):
    query = """
        INSERT INTO people_count_snapshots (schedule_id, camera_id, people_counter, captured_at, image_path)
        VALUES (%s, %s, %s, %s, %s);
    """
    
    try:
        conn=get_connection()
        cur=conn.cursor()

        cur.execute(query,(schedule_id,camera_id,people_couter,captured_at,image_path,))
        conn.commit()
        print(f"Inserted snapshot successfully: schedule_id={schedule_id}, camera_id={camera_id}, "
              f"people_counter={people_couter}, captured_at={captured_at}, image_path={image_path}")

    except Exception as e:
        print(f"Error when get camra ip:{e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
