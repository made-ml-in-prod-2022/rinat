from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.filesystem import FileSensor
from pendulum import today

from utils import default_args, DEFAULT_VOLUME


with DAG(
        "2_train_model",
        default_args=default_args,
        schedule_interval="@weekly",
        start_date=today("UTC").add(days=-3),
) as dag:
    start_task = EmptyOperator(task_id="begin-train-pipeline")
    data = FileSensor(
        task_id="await-features",
        poke_interval=10,
        retries=100,
        filepath="data/raw/{{ ds }}/data.csv",
    )
    split = DockerOperator(
        task_id="split-data",
        image="airflow-split",
        command="--input-dir /data/raw/{{ ds }}"
                "--output-dir /data/split/{{ ds }}"
                "--test_size 0.2",
        network_mode="bridge",
        do_xcom_push=False,
        volumes=[DEFAULT_VOLUME],
    )
    preprocess = DockerOperator(
        task_id="preprocess-data",
        image="airflow-preprocess",
        command="--input-dir /data/split/{{ ds }}"
                "--output-dir /data/processed/{{ ds }}"
                "--preprocessor-path /data/preprocessor/{{ ds }}",
        network_mode="bridge",
        do_xcom_push=False,
        volumes=[DEFAULT_VOLUME],
    )
    train = DockerOperator(
        task_id="train-model",
        image="airflow-train",
        command="--data-dir /data/processed/{{ ds }}"
                "--model-path /data/model/{{ ds }}",
        network_mode="host",
        do_xcom_push=False,
        volumes=DEFAULT_VOLUME,
    )
    validate = DockerOperator(
        task_id="evaluate-model",
        image="airflow-validate",
        command="--data-dir /data/split/{{ ds }}"
                "--preprocessor-path /data/preprocessor/{{ ds }}"
                "--model-path /data/model/{{ ds }}",
        network_mode="host",
        do_xcom_push=False,
        volumes=DEFAULT_VOLUME,
    )
    end_task = EmptyOperator(task_id="end-train-pipeline")

    (
        start_task
        >> data
        >> split
        >> preprocess
        >> train
        >> validate
        >> end_task
    )