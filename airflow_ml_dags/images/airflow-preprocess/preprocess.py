import os
import joblib

import click
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


@click.command("preprocess")
@click.option("--input-dir")
@click.option("--output-dir")
@click.option(
    '--preprocessor-path',
    envvar='PREPROCESSOR_PATH',
    type=click.Path(exists=True),
    required=True
)
def preprocess(input_dir: str, output_dir: str, preprocessor_path: str) -> None:
    """Preprocess data input

    Args:
        input_dir (str): input data directory
        output_dir (str):  output data directory
        preprocessor_path (str): directory to a preprocessing checkpoint

    Returns:
        None
    """
    # Load data
    df = pd.read_csv(os.path.join(input_dir, "train.csv"))
    X, y = df.drop(columns=["target"]), np.array(df["target"])

    # Preprocessing
    preprocessor = StandardScaler()
    df = preprocessor.fit_transform(X)
    df["target"] = y

    # Check output directories
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(preprocessor_path, exist_ok=True)

    # Save output
    df.to_csv(os.path.join(output_dir, "data.csv"))
    joblib.dump(preprocessor, os.path.join(preprocessor_path, "preprocessor.pkl"))


if __name__ == "__main__":
    preprocess()
