import pendulum
from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.providers.docker.operators.docker import DockerOperator

from utils import default_args, DEFAULT_VOLUME

with DAG(
    dag_id="2_train_pipeline",
    start_date=pendulum.today('UTC').add(days=-3),
    schedule_interval="@daily",
    default_args=default_args,
) as dag:
    data = FileSensor(
        task_id="await-data",
        poke_interval=10,
        retries=100,
        filepath="data/raw/{{ ds }}/data.csv",
        fs_conn_id="fs_default"
    )

    split = DockerOperator(
        task_id="split-data",
        image="airflow-split",
        command="--input_dir /data/raw/{{ ds }}"
                " --output_dir /data/split/{{ ds }}"
                " --test_size 0.2",
        network_mode="bridge",
        do_xcom_push=False,
        volumes=[DEFAULT_VOLUME]
    )

    preprocess = DockerOperator(
        task_id="preprocess-data",
        image="airflow-preprocess",
        command="--input_dir /data/split/{{ ds }}"
                " --output_dir /data/processed/{{ ds }}"
                " --preprocessor_path /data/preprocessor/{{ ds }}",
        network_mode="bridge",
        do_xcom_push=False,
        volumes=[DEFAULT_VOLUME]
    )
    train = DockerOperator(
        task_id="model-train",
        image="airflow-train",
        command="--data_dir /data/processed/{{ ds }}"
                " --model_path /data/model/{{ ds }}",
        do_xcom_push=False,
        volumes=[DEFAULT_VOLUME]
    )

    validate = DockerOperator(
        task_id="model-evaluation",
        image="airflow-validate",
        command="--data_dir /data/split/{{ ds }}"
                " --preprocessor_path /data/preprocessor/{{ ds }}"
                " --model_path /data/model/{{ ds }}",
        do_xcom_push=False,
        volumes=[DEFAULT_VOLUME]
    )

    (
            data
            >> split
            >> preprocess
            >> train
            >> validate
    )