import os
import joblib

import click
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


@click.command(name="train")
@click.option("--data_dir")
@click.option("--model_path")
def train(data_dir: str, model_path: str) -> None:
    """
    Train Logistic Regression model
    Args:
        data_dir (str): input data directory
        model_path (str): output model directory
    Returns:
        None
    """
    df = pd.read_csv(os.path.join(data_dir, "data.csv"), index_col=0)
    y = np.array(df["target"])
    X = df.drop(columns=["target"])

    model = RandomForestClassifier()
    model.fit(X, y)

    os.makedirs(model_path, exist_ok=True)
    joblib.dump(model, os.path.join(model_path, "model.pkl"))

if __name__ == "__main__":
    train()