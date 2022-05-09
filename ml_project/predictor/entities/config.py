import os
from dataclasses import dataclass
from typing import Any, Tuple

from hydra.core.config_store import ConfigStore


@dataclass
class Data:
    _target_: str = "predictor.data.data.DataPreprocessor"
    file_path: str = os.path.join(os.getcwd(),
                                  "data/heart_cleveland_upload.csv")
    shuffle: bool = True
    test_size: float = 0.2
    target: str = "condition"


@dataclass
class Metrics:
    _target_: str = "predictor.metrics.metrics.metrics"


@dataclass
class Model:
    _target_: str = "predictor.models.models.LR"


@dataclass
class Pipeline:
    _target_: str = "predictor.pipeline.pipeline.ModelPipeline"
    cat_features: Tuple[str] = ("sex", "fbs", "restecg", "exang", "slope",
                                "ca", "thal")
    num_features: Tuple[str] = ("age", "cp", "trestbps", "chol", "thalach",
                                "oldpeak")
    model: Any = Model()


@dataclass
class Config:
    original_work_dir: str
    seed: int = 42
    name: str = "classification_model"
    checkpoint_file: str = os.path.join(os.getcwd(), "model_weights")
    ignore_warnings: bool = True
    save_checkpoint_file: bool = True
    logger: str = os.path.join(os.getcwd(), "configs/logger/logger.yaml")
    train: bool = True
    test: bool = True
    data: Any = Data()
    metrics: Any = Metrics()
    pipeline: Any = Pipeline()


@dataclass
class MLflowLogger:
    _target_: str = "predictor.logger.mlflow.MLflowLogger"
    experiment_name: str = "Classification"
    run_name: str = "${general.run_name}"
    tracking_uri: str = "${general.project_dir}/mlruns"


def register_configs() -> None:
    cs = ConfigStore.instance()
    cs.store(name="config", node=Config)
    cs.store(group="config/data", name="data", node=Data)
    cs.store(group="config/metrics", name="metrics", node=Metrics)
    cs.store(group="config/pipeline", name="pipeline", node=Pipeline)
    cs.store(group="config/logger", name="mlflow_logger", node=MLflowLogger)
