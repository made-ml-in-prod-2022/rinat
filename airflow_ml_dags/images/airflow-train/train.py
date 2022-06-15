import os
import joblib

import click
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression


@click.command("train")
@click.option("--data-dir")
@click.option("--model-path")
def train(data_dir: str, model_path: str) -> None:

    df = pd.read_csv(os.path.join(data_dir, "data.csv"))
    X, y = df.drop(columns=["target"]), np.array(df["target"])


    model = LogisticRegression()
    model.fit(X, y)
    joblib.dump(model, os.path.join(model_path, "model.pkl"))

if __name__ == "__main__":
    train()
