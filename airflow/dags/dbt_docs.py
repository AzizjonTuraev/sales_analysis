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
    'get_dbt_docs',
    default_args=default_args,
    description='Getting dbt docs',
    schedule_interval=None,
    start_date=datetime.today() - timedelta(days=1),
    catchup=False,
) as dag:

    # Task 1: Navigate to dbt project and run dbt seed
    get_dbt_docs = BashOperator(
        task_id='dbt_seed',
        bash_command='''
        export PATH=/home/airflow/.local/bin:$PATH
        cd /opt/airflow/commerce_dbt
        dbt docs generate
        ''',
        env={
            'DBT_PROFILES_DIR': '/opt/airflow/commerce_dbt'  # Point to your profiles.yml location
        }
    )


