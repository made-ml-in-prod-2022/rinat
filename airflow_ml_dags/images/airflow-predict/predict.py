import os
import joblib

import click
import numpy as np
import pandas as pd


@click.command(name="predict")
@click.option("--input_dir")
@click.option("--output_dir")
@click.option(
    '--preprocessor_path',
    type=click.Path(exists=True),
    required=True
)
@click.option(
    '--model_path',
    type=click.Path(exists=True),
    required=True
)
def predict(input_dir: str, output_dir: str, preprocessor_path: str, model_path: str) -> None:
    """
    Make prediction and save output into output directory
    Args:
        input_dir (str): input data directory
        output_dir (str): output data directory
        preprocessor_path (str): directory to a preprocessing checkpoint
        model_path (str): directory to a model checkpoint
    Returns:
        None
    """
    # Load df
    df = pd.read_csv(os.path.join(input_dir, "data.csv"), index_col=0)
    if "target" in df.columns:
        df = df.drop(columns=["target"])
    X = df.copy()
    # Load preprocessor and model
    preprocessor = joblib.load(os.path.join(preprocessor_path, "preprocessor.pkl"))
    model = joblib.load(os.path.join(model_path, "model.pkl"))

    # Make predictions
    df["predict"] = np.array(model.predict(preprocessor.transform(X)))

    # Output df
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(os.path.join(output_dir, "predictions.csv"))


if __name__ == "__main__":
    predict()