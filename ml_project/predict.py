import hydra
from omegaconf import DictConfig
import logging
import logging.config
import yaml


def setup_logging(logging_yaml_config_fpath):
    """setup logging via YAML if it is provided"""
    if logging_yaml_config_fpath:
        with open(logging_yaml_config_fpath) as config_fin:
            logging.config.dictConfig(yaml.safe_load(config_fin))


@hydra.main(config_path="configs/", config_name="predict.yaml")
def main(config: DictConfig):

    # Imports can be nested inside @hydra.main to optimize tab completion
    # https://github.com/facebookresearch/hydra/issues/934
    from predictor.engine.trainer import predict
    setup_logging(config.logger)
    # Inference model
    return predict(config)


if __name__ == "__main__":
    main()