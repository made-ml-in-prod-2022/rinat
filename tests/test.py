from .dataset_generator import generate_dataset
from ml_project.predictor.data.data import DataPreprocessor
from ml_project.predictor.pipeline.pipeline import ModelPipeline
from ml_project.predictor.models.models import LR, RF
import tempfile
import os
import pytest

CAT_FEATURES = ["sex", "fbs", "restecg", "exang", "slope", "ca", "thal"]
NUM_FEATURES = ["age", "cp", "trestbps", "chol", "thalach", "oldpeak"]


@pytest.mark.parametrize("test_input,expected", [(10, 5), (100, 50)])
def test_data_processor(test_input, expected):
    with tempfile.TemporaryDirectory() as tmpdirname:
        df = generate_dataset(test_input)
        filename = os.path.join(tmpdirname, "temp.csv")
        df.to_csv(filename)
        data = DataPreprocessor(filename, True, 0.5, "condition")
        X_train, y_train, X_val, y_val = data.process()
        assert (
            len(X_train) == expected
        ), f"Expected dataset len is {expected}, but got {len(X_train)}"


@pytest.mark.parametrize(
    "features,num",
    [([CAT_FEATURES, NUM_FEATURES], 10), ([CAT_FEATURES, NUM_FEATURES], 100)],
)
def test_model_pipeline(features, num):
    with tempfile.TemporaryDirectory() as tmpdirname:
        df = generate_dataset(num)
        filename = os.path.join(tmpdirname, "temp.csv")
        df.to_csv(filename)
        data = DataPreprocessor(filename, True, 0.5, "condition")
        X_train, y_train, X_val, y_val = data.process()
        model = LR()
        pipeline = ModelPipeline(features[0], features[1], model)
        pipe = pipeline.get_pipeline()
        assert pipe is not None, "The pipeline is not working properly"
        pipe.fit(X_train, y_train)
        y_preds = pipe.predict(X_val)
        assert len(y_preds) == len(y_val)


@pytest.mark.parametrize("test_input", [10, 100])
def test_model_abc(test_input):
    with tempfile.TemporaryDirectory() as tmpdirname:
        df = generate_dataset(test_input)
        filename = os.path.join(tmpdirname, "temp.csv")
        df.to_csv(filename)
        data = DataPreprocessor(filename, True, 0.5, "condition")
        X_train, y_train, X_val, y_val = data.process()
        models = [LR(), RF()]
        for model in models:
            model.fit(X_train, y_train)
            y_preds = model.predict(X_val)
            assert len(y_preds) == len(y_val)
