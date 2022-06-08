import logging

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

logger = logging.getLogger(__name__)


class ModelPipeline:

    def __init__(self, cat_features, num_features, model):
        self.cat_features = list(cat_features)
        self.num_features = list(num_features)
        self.model = model
        self.name = self.model.name
        logger.info("The model is initialized")

    def get_pipeline(self):
        numeric_transformer = Pipeline(steps=[("MinMaxScaler",
                                               MinMaxScaler())])

        categorical_transformer = OneHotEncoder(handle_unknown="ignore")

        preprocessor = ColumnTransformer(transformers=[
            ("num", numeric_transformer, self.num_features),
            ("cat", categorical_transformer, self.cat_features),
        ])
        pipe = Pipeline(steps=[('preprocessor',
                                preprocessor), ('model', self.model)])
        return pipe
