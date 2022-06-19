import os
import joblib

import click
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


@click.command(name="preprocess")
@click.option("--input_dir")
@click.option("--output_dir")
@click.option('--preprocessor_path')
def preprocess(input_dir: str, output_dir: str, preprocessor_path: str) -> None:
    """
    Preprocess data input
    Args:
        input_dir (str): input data directory
        output_dir (str):  output data directory
        preprocessor_path (str): directory to a preprocessing checkpoint
    Returns:
        None
    """
    # Load data
    df = pd.read_csv(os.path.join(input_dir, "train.csv"), index_col=0)
    y = np.array(df["target"].values)
    X = df.drop(columns=["target"])
    columns = list(X.columns)
    # Preprocessing
    preprocessor = StandardScaler()
    df = preprocessor.fit_transform(X)
    df = pd.DataFrame(data=df, columns=columns)
    df["target"] = y

    # Check output directories
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(preprocessor_path, exist_ok=True)

    # Save output
    df.to_csv(os.path.join(output_dir, "data.csv"))
    joblib.dump(preprocessor, os.path.join(preprocessor_path, "preprocessor.pkl"))


if __name__ == "__main__":
    preprocess()