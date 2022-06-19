from datetime import timedelta

import airflow
from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago

from utils import default_args, DEFAULT_VOLUME

with DAG(
    dag_id="3_inference",
    start_date=airflow.utils.dates.days_ago(5),
    schedule_interval="@daily",
    default_args=default_args,
) as dag:
    data_await = FileSensor(
        task_id="await-data",
        poke_interval=10,
        retries=100,
        filepath="data/raw/{{ ds }}/data.csv",
        fs_conn_id="fs_default"
    )

    # training_pipeline = ExternalTaskSensor(
    #     task_id="training_pipeline",
    #     external_dag_id="2_train_pipeline",
    #     external_task_id='model-evaluation',
    #     check_existence=True,
    #     execution_delta=timedelta(days=1),
    #     timeout=120,
    # )

    prediction = DockerOperator(
        task_id="generate-predicts",
        image="airflow-predict",
        command="--input_dir /data/raw/{{ ds }}"
                " --output_dir /data/predictions/{{ ds }}"
                " --preprocessor_path /data/preprocessor/{{ ds }}"
                " --model_path /data/model/{{ ds }}",
        do_xcom_push=False,
        volumes=[DEFAULT_VOLUME]
    )


    (
            data_await
            >> prediction
    )