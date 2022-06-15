import os
import joblib

import pandas as pd
import click


@click.command("predict")
@click.option("--input-dir")
@click.option("--output-dir")
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
def predict(input_dir: str, output_dir: str, preprocessor_path: str, model_path: str) -> None:
    """Make prediction and save output into output directory

    Args:
        input_dir (str): input data directory
        output_dir (str): output data directory
        preprocessor_path (str): directory to a preprocessing checkpoint
        model_path (str): directory to a model checkpoint

    Returns:
        None
    """
    # Load data
    data = pd.read_csv(os.path.join(input_dir, "data.csv"), index_col=0)

    # Load preprocessor and model
    preprocessor = joblib.load(os.path.join(preprocessor_path, "preprocessor.pkl"))
    model = joblib.load(os.path.join(model_path, "model.pkl"))

    # Make predictions
    data["predict"] = model.predict(preprocessor.transform(data))

    # Output data
    os.makedirs(output_dir, exist_ok=True)
    data.to_csv(os.path.join(output_dir, "predictions.csv"))


if __name__ == "__main__":
    predict()