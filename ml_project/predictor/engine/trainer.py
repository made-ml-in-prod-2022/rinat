import os.path
from typing import NoReturn
import random
import numpy as np
from hydra.utils import instantiate
import pickle
from predictor.utils.utils import set_global_seed
import logging


logger = logging.getLogger("logs")


def train(config):
    if config.seed  is not None:
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

    if config.save_checkpoint_file:
        if not os.path.exists(config.checkpoint_file):
            os.mkdir(config.checkpoint_file)

        filename = os.path.join(config.checkpoint_file, pipeline.name)

        with open(filename, 'wb') as file:
            pickle.dump(model_pipeline, file)