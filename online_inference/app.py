#!/usr/bin/env python
'''
coding: utf-8 -*-
----------------------------------------------------------------------------
Author: Xrenya
Created Date: 28.05.2022 17:10
version ='1.0'
---------------------------------------------------------------------------
'''
import logging
import os

import joblib
import uvicorn
from fastapi import FastAPI

from config.config import config
from src.utils import ConditionModel, ModelResponse, prediction, setup_logging

app = FastAPI(title="Heart Disease Model API",
              description="A simple model to make a Heart Disease Condition",
              version="0.0.1")
model = None
transformer = None
cfg = config
setup_logging(cfg.logger)
logger = logging.getLogger("logs")


@app.on_event('startup')
def load_model():
    """Loads models at startup of the app"""
    logger.info('Loading model...')
    model_path = os.path.join(os.getcwd(), cfg.model_checkpoint_file)
    transformer_path = os.path.join(os.getcwd(),
                                    cfg.transformer_checkpoint_file)
    if model_path is None or transformer_path is None:
        error = "Model weights are not provided, 'model_path'" \
            "is None or 'transformer_path' is None"
        logger.error(
            "Model weights are not provided, 'model_path' is "
            f"{model_path} or transformer_path is {transformer_path}"
        )
        raise RuntimeError(error)
    global model, transformer
    model = joblib.load(model_path)
    transformer = joblib.load(transformer_path)
    logger.info('Model is successfully loaded and ready for inference')


@app.get('/')
async def root():
    """Root app message"""
    return {
        'message':
        "Heart Disease Classificator. Available commands see in '/docs'"
    }


@app.get('/health')
async def health_check():
    """Health checkup of the app"""
    logger.info("The model is ready for inference")
    if model and transformer:
        return 200
    else:
        return 204


@app.get('/predict', response_model=ModelResponse)
async def predict(request: ConditionModel):
    """Function for model inference"""
    logger.info("Making predictions...")
    output = prediction(request.data, request.feature_names, model,
                        transformer)
    return output


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.getenv("PORT", 5000))
