from airflow import DAG
from airflow.operators.python import PythonOperator
import psycopg2
from datetime import datetime, timedelta
from io import StringIO
import csv
from airflow.models import Variable

from airflow.operators.trigger_dagrun import TriggerDagRunOperator 

default_args = {
    "owner": "azizjon",
    "retries": 0,
    "retry_delay": timedelta(minutes=5)
}


def load_new_order_items(**context):

    conn = psycopg2.connect(
        host="host.docker.internal",
        database="postgres",
        user=Variable.get("user_postgres"),
        password=Variable.get("password_postgres"),
        port="5432"
    )
    cursor = conn.cursor()
    clean_data = None
    
    try:
        clean_data = StringIO()
        
        csv_file_path = '/opt/airflow/dataset/new_dataset/new_order_items.csv'
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
        CREATE TEMP TABLE temp_new_order_items (LIKE commerce_raw.order_items) ON COMMIT DROP;
        """)
        
        # Load into temp table
        cursor.copy_expert("COPY temp_new_order_items FROM stdin WITH CSV HEADER DELIMITER ','", clean_data)
        
        cursor.execute("""
        INSERT INTO commerce_raw.order_items
        SELECT * FROM temp_new_order_items;
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
    dag_id="load_new_order_items",
    default_args=default_args,
    start_date=datetime.today() - timedelta(days=1),
    # schedule_interval=None,
    schedule_interval="5 * * * Mon-Sat",
    catchup=False,
    max_active_runs=1  # Prevent overlapping runs
) as dag:

    load_task = PythonOperator(
        task_id='load_new_order_items',
        python_callable=load_new_order_items,
        execution_timeout=timedelta(minutes=10)  # Set timeout
    )

