import psycopg2
from prefect import task

from prefect import task
import psycopg2

@task
def setup_database():
    conn = psycopg2.connect(
        host="192.168.56.1",
        dbname="postgres",
        user="postgres",
        password="Newpassword",
        port="5433"
    )
    cur = conn.cursor()
    
    sql_files = ['./sql_scripts/raw.sql', './sql_scripts/archived.sql', './sql_scripts/cleansed.sql']
    for sql_file in sql_files:
        with open(sql_file, 'r') as file:
            sql_script = file.read()
        cur.execute(sql_script)
    
    conn.commit()
    cur.close()
    conn.close()