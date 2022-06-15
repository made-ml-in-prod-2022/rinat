from datetime import timedelta
import os

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.filesystem import FileSensor
from airflow.sensors.external_task import ExternalTaskSensor
from pendulum import today

from utils import default_args, DEFAULT_VOLUME, ARTIFACT_VOLUME, mlflow_env, model_name


with DAG(
        "3_make_predicts",
        default_args=default_args,
        schedule_interval="@daily",
        start_date=today("UTC").add(days=-3),
) as dag:
    start_task = EmptyOperator(task_id="begin-inference")
    data_await = FileSensor(
        task_id="await-features",
        poke_interval=10,
        retries=100,
        filepath="data/raw/{{ ds }}/data.csv",
    )
    scaler_await = FileSensor(
        task_id="await-scaler",
        poke_interval=10,
        retries=100,
        filepath="data/preprocessor/{{ ds }}/preprocessor.pkl",
    )
    train_await = ExternalTaskSensor(
        task_id="await-training",
        external_dag_id="2_train_model",
        check_existence=True,
        execution_delta=timedelta(days=1),
        timeout=120,
    )
    predict = DockerOperator(
        task_id="generate-predicts",
        image="airflow-predict",
        command="--input-dir /data/raw/{{ ds }}"
                "--output-dir /data/predictions/{{ ds }}"
                "--preprocessor-path /data/preprocessor/{{ ds }}"
                "--model-path /data/model/{{ ds }}",
        network_mode="host",
        private_environment=mlflow_env,
        do_xcom_push=False,
        volumes=[DEFAULT_VOLUME, ARTIFACT_VOLUME],
    )
    end_task = EmptyOperator(task_id="end-inference")

    (
            start_task
            >> [data_await, scaler_await]
            >> train_await
            >> predict
            >> end_task
    )