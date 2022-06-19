from datetime import timedelta



default_args = {
    "owner": "admin",
    "email_on_failure": False,
    "email": ["admin@example.com"],
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

DEFAULT_VOLUME = "/home/xrenya/Documents/MADE/MLProd/airflow/test/data:/data"
