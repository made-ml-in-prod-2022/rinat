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

from src.utils import setup_logging
from config.config import config
from config.base_config import Config


app = FastAPI()
logger = logging.getLogger("logs")


@app.get('/')
async def root():
    return {'message': "Heart Disease Classificator. Available commands see in '/docs'"}


@app.get('/health')
async def health_check():
    logger.info("The model is ready for inference")
    return 200


def setup_logger(config: Config):
    setup_logging(config.logger)

if __name__ == "__main__":
    cfg = config
    setup_logger(cfg)
    uvicorn.run(
        app, host="0.0.0.0", port=os.getenv("PORT", 5000)
    )