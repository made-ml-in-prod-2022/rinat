import pendulum
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

from utils import default_args, DEFAULT_VOLUME

with DAG(
    dag_id="1_generate_data",
    start_date=pendulum.today('UTC').add(days=-3),
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
