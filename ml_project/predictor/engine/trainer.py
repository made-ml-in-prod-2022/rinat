import logging
import os.path

import joblib
from hydra.utils import instantiate

from predictor.entities.config import Config
from predictor.utils.utils import set_global_seed

logger = logging.getLogger(__name__)


def train(config: Config):
    mlflow_logger = instantiate(config.logger)

    if config.seed is not None:
        set_global_seed(config.seed)
        logger.info(f"The global random seed is fixed {config.seed}")

    data_processor = instantiate(config.data)
    X_train, y_train, X_val, y_val = data_processor.process()

    pipeline = instantiate(config.pipeline)
    model_pipeline = pipeline.get_pipeline()
    logger.info(f"Model fitting")
    model_pipeline.fit(X_train, y_train)

    logger.info(f"Model prediction on validation dataset")
    y_preds = model_pipeline.predict(X_val)

    metrics = instantiate(config.metrics)
    for metric, func in metrics.items():
        output_metric = func(y_val, y_preds)
        logger.info(f"{metric} on validation dataset: {output_metric}")
        if mlflow_logger is not None:
            mlflow_logger.log_metric(metric, output_metric)

    if config.save_checkpoint_file:
        if not os.path.exists(config.checkpoint_file):
            os.mkdir(config.checkpoint_file)

        filename = os.path.join(config.checkpoint_file, pipeline.name + ".pkl")
        logger.info(f"Saving pipeline into {filename}")

        joblib.dump(model_pipeline, filename)

        if mlflow_logger is not None:
            mlflow_logger.log_sklearn_model(model_pipeline,
                                            "log_sklearn_model")
            mlflow_logger.end_run()


def predict(config: Config):
    if config.seed is not None:
        set_global_seed(config.seed)
        logger.info(f"The global random seed is fixed {config.seed}")

    data_processor = instantiate(config.data)
    X = data_processor.inference_process()

    logger.info(f"Loading model from {config.checkpoint_file}")
    model_pipeline = joblib.load(config.checkpoint_file)

    logger.info(f"Model prediction on dataset")
    y_preds = model_pipeline.predict(X)

    if not os.path.exists(config.csv_output):
        os.mkdir(config.csv_output)

    filename = os.path.join(config.csv_output, config.csv_filename)

    logger.info(f"Saving output into {filename}")

    with open(filename, "w") as f:
        f.write("\n".join(y_preds.astype(str)))
