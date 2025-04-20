from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "azizjon",
    "retries": 0,
    "email_on_failure" : False,
    "email_on_retry": False,
    "retries" : 0,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    'dbt_etl_pipeline_test',
    default_args=default_args,
    description='ETL pipeline running dbt commands',
    schedule_interval="@daily",
    start_date=datetime.today() - timedelta(days=1),
    catchup=False,
) as dag:

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='''
        export PATH=/home/airflow/.local/bin:$PATH
        cd /opt/airflow/commerce_dbt
        dbt test --profiles-dir .
        ''',
        env={
            'DBT_PROFILES_DIR': '/opt/airflow/commerce_dbt'  # Point to your profiles.yml location
        }
    )
