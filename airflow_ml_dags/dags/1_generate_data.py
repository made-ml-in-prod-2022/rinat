from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.docker.operators.docker import DockerOperator
from pendulum import today
from docker.types import Mount

from utils import default_args, DEFAULT_VOLUME


with DAG(
        "1_generate_data",
        default_args=default_args,
        schedule_interval="@daily",
        start_date=today("UTC").add(days=-3),
) as dag:
    start_task = EmptyOperator(task_id="begin-generate-data")
    download_data = DockerOperator(
        task_id="docker-airflow-download",
        image="airflow-download",
        command="output-dir /data/raw/{{ ds }}",
        network_mode="bridge",
        do_xcom_push=False,
        volumes=[Mount("/home/xrenya/Documents/MADE/MLProd/airflow/rinat-homework3/airflow_ml_dags/data", target="/data", type='bind')],
    )

    end_task = EmptyOperator(task_id="end-generate-data")

    start_task >> download_data >> end_task