import os

import click
from sklearn.datasets import load_breast_cancer


@click.command(name="download")
@click.argument("--output")
def main(output: str):
    X, y = load_breast_cancer(return_X_y=True, as_frame=True)
    os.makedirs(output, exist_ok=True)
    X.to_csv(os.path.join(output, "data.csv"))
    y.to_csv(os.path.join(output, "target.csv"))

if __name__ == "__main__":
    main()
