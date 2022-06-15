import os
import joblib

import click
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score


@click.command("validate")
@click.option("--data-dir")
@click.option(
    '--preprocessor-path',
    envvar='PREPROCESSOR_PATH',
    type=click.Path(exists=True),
    required=True
)
@click.option(
    '--model-path',
    envvar='MODEL_PATH',
    type=click.Path(exists=True),
    required=True
)
def validate(data_dir: str, preprocessor_path: str, model_path: str) -> None:
    """Validate the model and output metrics

    Args:
        data_dir (str): input data directory
        preprocessor_path (str): directory to a preprocessing checkpoint
        model_path (str): directory to a model checkpoint

    Returns:

    """
    # Should include logger here and the rest of the files, no information is bad

    # Load data
    df = pd.read_csv(os.path.join(data_dir, "validation.csv"))
    X, y = df.drop(columns=["target"]), np.array(df["target"])

    # Load preprocessor and model
    preprocessor = joblib.load(os.path.join(preprocessor_path, "preprocessor.pkl"))
    model = joblib.load(os.path.join(model_path, "model.pkl"))

    # Make predictions
    preds = model.predict(preprocessor.transform(X))

    # Output data
    print("roc_auc_score", roc_auc_score(y, preds))
    print("accuracy_score", accuracy_score(y, preds))
    print("f1_score", f1_score(y, preds))


if __name__ == "__main__":
    validate()
