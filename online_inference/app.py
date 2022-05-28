#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Author: Xrenya
# Created Date: 28.05.2022 17:10
# version ='1.0'
# ---------------------------------------------------------------------------
import os
import uvicorn
from fastapi import FastAPI
import logging
import joblib

from src.utils import setup_logging
from config.config import config
from config.base_config import Config


app = FastAPI()
model_pipeline = None
logger = logging.getLogger("logs")


@app.on_event('startup')
def load_model(cfg: Config):
    """Loads model at startup of the app"""
    logger.info('Loading model...')
    model_path = cfg.checkpoint_file
    if model_path is None:
        error = f"Model weights are not provided, 'model_path' is None"
        logger.error(f"Model weights are not provided, 'model_path' is None")
        raise RuntimeError(error)
    global model_pipeline
    model_pipeline = joblib.load(model_path)
    logger.info(f'Model is successfully loaded and ready for inference')


@app.get('/')
async def root():
    return {'message': "Heart Disease Classificator. Available commands see in '/docs'"}


@app.get('/health')
async def health_check():
    logger.info("The model is ready for inference")
    if model_pipeline:
        return 200
    else:
        return 204


def setup_logger(cfg: Config):
    setup_logging(cfg.logger)


if __name__ == "__main__":
    cfg = config
    setup_logger(cfg)
    print(cfg)
    load_model(cfg)
    uvicorn.run(
        app, host="0.0.0.0", port=os.getenv("PORT", 5000)
    )