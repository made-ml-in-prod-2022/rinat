import logging
import logging.config
from typing import List, Union

import numpy as np
import pandas as pd
import yaml
from fastapi import HTTPException
from pydantic import BaseModel, conlist
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression

logger = logging.getLogger("logs")


def setup_logging(logging_yaml_config_fpath):
    """setup logging via YAML if it is provided"""
    if logging_yaml_config_fpath:
        with open(logging_yaml_config_fpath) as config_fin:
            logging.config.dictConfig(yaml.safe_load(config_fin))


class ModelResponse(BaseModel):
    """Model output dataclass"""
    condition: List[int]


class ConditionModel(BaseModel):
    """Model input dataclass"""
    data: List[conlist(Union[float, int, None], min_items=13, max_items=13)]
    feature_names: List[str]


def prediction(
    data: List,
    feature_names: List[str],
    model: LogisticRegression,
    transformer: ColumnTransformer,
) -> ModelResponse:
    """Prediction function"""
    if len(data) == 0:
        raise HTTPException(status_code=400, detail="Input should not be empty")
    data = pd.DataFrame(np.array(data), columns=feature_names)
    data = transformer.transform(data)
    transformed_df = pd.DataFrame(data)
    preds = list(model.predict(transformed_df))
    return ModelResponse(condition=preds)