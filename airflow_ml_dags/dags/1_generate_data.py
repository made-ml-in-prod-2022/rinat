import airflow

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago

from utils import default_args, DEFAULT_VOLUME

with DAG(
    dag_id="1_generate_data",
    start_date=airflow.utils.dates.days_ago(5),
    schedule_interval="@daily",
    default_args=default_args,
) as dag:
    download = DockerOperator(
        image="airflow-download",
        command="/data/raw/{{ ds }}",
        network_mode="bridge",
        task_id="docker-airflow-download",
        do_xcom_push=False,
        volumes=[DEFAULT_VOLUME]
    )


    download
