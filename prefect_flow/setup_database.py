import psycopg2
from prefect import task, flow

@task
def connect_to_db():
    conn = psycopg2.connect(
        host="192.168.56.1",
        dbname="postgres",
        user="postgres",
        password="Newpassword",
        port="5433"
    )
    return conn

@task
def execute_sql_script(conn, sql_file):
    cur = conn.cursor()
    with open(sql_file, 'r') as file:
        sql_script = file.read()
    cur.execute(sql_script)
    conn.commit()
    cur.close()

@task
def close_db_connection(conn):
    conn.close()

@flow
def connect_and_setup():
    conn = connect_to_db()
    
    sql_files = ['./sql_scripts/raw.sql', './sql_scripts/archived.sql', './sql_scripts/cleansed.sql', '.sql_scripts/wareahouse.sql']
    for sql_file in sql_files:
        execute_sql_script(conn, sql_file)
    
    close_db_connection(conn)

