from airflow import DAG
from airflow.operators.python import PythonOperator
import psycopg2
from datetime import datetime, timedelta
from io import StringIO
import csv

from airflow.operators.trigger_dagrun import TriggerDagRunOperator 

default_args = {
    "owner": "azizjon",
    "retries": 0,
    "retry_delay": timedelta(minutes=5)
}



def load_new_orders(**context):

    conn = psycopg2.connect(
        host="host.docker.internal",
        database="postgres",
        user="postgres",
        password="PostgreSQL32",
        port="5432"
    )
    cursor = conn.cursor()
    clean_data = None
    
    try:
        clean_data = StringIO()
        
        csv_file_path = '/opt/airflow/dataset/new_dataset/new_orders.csv'
        with open(csv_file_path, 'r') as f:
            reader = csv.reader(f)
            writer = csv.writer(clean_data)
            header = next(reader)
            writer.writerow(header)
            
            for row in reader:
                writer.writerow(row)

        clean_data.seek(0)
        
        # Create temp table
        cursor.execute("""
        CREATE TEMP TABLE temp_new_orders (LIKE commerce_raw.orders) ON COMMIT DROP;
        """)
        
        # Load into temp table
        cursor.copy_expert("COPY temp_new_orders FROM stdin WITH CSV HEADER DELIMITER ','", clean_data)
        
        # Insert with duplicate handling (replace 'order_id' with your PK)
        cursor.execute("""
        INSERT INTO commerce_raw.orders
        SELECT * FROM temp_new_orders;
        """)
                
        conn.commit()
        
    except Exception as e:
        print(f"Error loading orders: {str(e)}")
        if conn:
            conn.rollback()
        raise

    cursor.close()
    conn.close()
    clean_data.close()



with DAG(
    dag_id="load_new_orders",
    default_args=default_args,
    start_date=datetime.today() - timedelta(days=1),
    schedule_interval="0 * * * Mon-Sat",
    # schedule_interval=None,
    catchup=False
) as dag:

    load_task = PythonOperator(
        task_id='load_new_orders',
        python_callable=load_new_orders,
    )

