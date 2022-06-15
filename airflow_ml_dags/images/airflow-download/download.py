import os

import click
import pandas as pd
from sklearn.datasets import load_wine


@click.command("download")
@click.argument("--output-dir")
def download(output_dir: str):
    """Download wine dataset (load_wine) from sklearn.datasets
    
    Args:
        output_dir (str): output directory to save the dataset in csv format
    """
    data = load_wine()
    df = pd.DataFrame(data=data["data"], columns=data['feature_names'])
    df["target"] = data["target"]

    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(os.path.join(output_dir, "data.csv"))


if __name__ == '__main__':
    download()
