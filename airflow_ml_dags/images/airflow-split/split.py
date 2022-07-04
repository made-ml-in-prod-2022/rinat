import os
from typing import Optional

import click
import pandas as pd
from sklearn.model_selection import train_test_split


@click.command(name="split")
@click.option("--input_dir")
@click.option("--output_dir")
@click.option("--test_size")
def split(input_dir: str, output_dir: str, test_size: Optional[float] = 0.2):
    """Split dataset into train/validation sets save output into output directory

    Args:
        input_dir (str): input data directory
        output_dir (str): output data directory
        test_size (Optional[float]): size of test size

    Returns:
        None
    """
    data = pd.read_csv(os.path.join(input_dir, "data.csv"), index_col=0)
    train, val = train_test_split(data, test_size=float(test_size))

    os.makedirs(output_dir, exist_ok=True)
    train.to_csv(os.path.join(output_dir, "train.csv"))
    val.to_csv(os.path.join(output_dir, "validation.csv"))


if __name__ == "__main__":
    split()