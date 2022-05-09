from abc import ABC, abstractmethod

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


class Model(ABC):

    @abstractmethod
    def __init__(self):
        super().__init__()
        self.model = None
        self.name = type(self).__name__

    def fit(self, x, y):
        self.model.fit(x, y)

    def fit_predict(self, x_train, y_train, x):
        self.model.fit(x_train, y_train)
        y_preds = self.model.predict(x)
        return y_preds

    def predict(self, x):
        y_preds = self.model.predict(x)
        return y_preds


class LR(Model):

    def __init__(self, **kwargs):
        super().__init__()
        self.model = LogisticRegression(**kwargs)


class RF(Model):

    def __init__(self, **kwargs):
        super().__init__()
        self.model = RandomForestClassifier(**kwargs)
