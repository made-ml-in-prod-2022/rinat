import os

import click
from sklearn.datasets import load_wine


@click.command("download")
@click.argument("output_dir")
def download(output_dir: str):
    """Download wine dataset (load_wine) from sklearn.datasets
    
    Args:
        output_dir (str): output directory to save the dataset in csv format
    """
    X, y = load_wine(return_X_y=True, as_frame=True)

    os.makedirs(output_dir, exist_ok=True)
    X.to_csv(os.path.join(output_dir, "data.csv"))


if __name__ == '__main__':
    download()
