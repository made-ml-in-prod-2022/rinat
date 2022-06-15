from datetime import timedelta
import os


default_args = {
    "owner": "airflow",
    "email_on_failure": True,
    "email": ["airflow@example.com"],  # "airflow@example.com"
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

DEFAULT_VOLUME = f"{os.getcwd()}/data"
