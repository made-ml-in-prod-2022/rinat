import logging

import mlflow


class MLflowLogger:

    def __init__(self, experiment_name: str, run_name: str, tracking_uri: str):
        mlflow.warnings.filterwarnings("ignore")
        mlflow.set_tracking_uri(tracking_uri)
        self.mlflow_run = None
        mlflow.set_experiment(experiment_name)
        experiment = mlflow.get_experiment_by_name(experiment_name)
        mlflow.start_run(run_name=run_name,
                         experiment_id=experiment.experiment_id)
        self.mlflow_run = mlflow.active_run()

        if self.mlflow_run:
            self.log_dict, self.current_epoch = {}, 0
            logging.info(f"[MlFlow] logging initiated successfully.")
        else:
            logging.warning(f"[Mlflow] MLflow is not run!")

    def log_param(self, *args, **kwargs):
        if self.mlflow_run:
            mlflow.log_param(*args, **kwargs)

    def log_params(self, *args, **kwargs):
        if self.mlflow_run:
            mlflow.log_params(*args, **kwargs)

    def log_metric(self, *args, **kwargs):
        if self.mlflow_run:
            mlflow.log_metric(*args, **kwargs)

    def log_metrics(self, *args, **kwargs):
        if self.mlflow_run:
            mlflow.log_metrics(*args, **kwargs)

    def log_artifact(self, *args, **kwargs):
        if self.mlflow_run:
            mlflow.log_artifact(*args, **kwargs)

    def log_artifacts(self, *args, **kwargs):
        if self.mlflow_run:
            mlflow.log_artifacts(*args, **kwargs)

    def log_sklearn_model(self, *args, **kwargs):
        if self.mlflow_run:
            mlflow.sklearn.log_model(*args, **kwargs)

    def end_run(self):
        if self.mlflow_run:
            mlflow.end_run()
