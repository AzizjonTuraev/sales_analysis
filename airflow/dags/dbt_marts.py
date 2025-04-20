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
    'dbt_etl_pipeline_mart',
    default_args=default_args,
    description='ETL pipeline running dbt commands',
    schedule_interval=None,  
    start_date=datetime.today() - timedelta(days=1),
    catchup=False,
) as dag:

    dbt_marts_core = BashOperator(
        task_id='dbt_marts_core',
        bash_command='''
        export PATH=/home/airflow/.local/bin:$PATH
        cd /opt/airflow/commerce_dbt
        dbt run --select marts.core --profiles-dir .
        ''',
        env={
            'DBT_PROFILES_DIR': '/opt/airflow/commerce_dbt'
        }
    )


    dbt_marts_business = BashOperator(
        task_id='dbt_marts_business',
        bash_command='''
        export PATH=/home/airflow/.local/bin:$PATH
        cd /opt/airflow/commerce_dbt
        dbt run --select marts.business --profiles-dir .
        ''',
        env={
            'DBT_PROFILES_DIR': '/opt/airflow/commerce_dbt'
        }
    )

    dbt_marts_core >> dbt_marts_business


