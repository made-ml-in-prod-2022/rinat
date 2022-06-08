import pandas as pd
from faker import Faker
from numpy.random import normal


def generate_dataset(n_rows: int):
    fake = Faker()
    fake_data = {
        "sex": fake.random_elements(elements=list(range(2)), length=n_rows),
        "cp": fake.random_elements(elements=list(range(4)), length=n_rows),
        "fbs": fake.random_elements(elements=list(range(2)), length=n_rows),
        "restecg": fake.random_elements(elements=list(range(3)), length=n_rows),
        "exang": fake.random_elements(elements=list(range(2)), length=n_rows),
        "slope": fake.random_elements(elements=list(range(3)), length=n_rows),
        "ca": fake.random_elements(elements=list(range(4)), length=n_rows),
        "thal": fake.random_elements(elements=list(range(3)), length=n_rows),
        "age": [normal(54.54, 9.05) for _ in range(n_rows)],
        "trestbps": [normal(131.69, 17.76) for _ in range(n_rows)],
        "chol": [normal(247.35, 52) for _ in range(n_rows)],
        "thalach": [normal(149.6, 22.94) for _ in range(n_rows)],
        "oldpeak": [normal(1.06, 1.17) for _ in range(n_rows)],
        "condition": fake.random_elements(elements=list(range(2)), length=n_rows),
    }

    fake_df = pd.DataFrame(fake_data)
    return fake_df
