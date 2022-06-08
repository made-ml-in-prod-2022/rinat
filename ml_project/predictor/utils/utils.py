from typing import NoReturn
import random
import numpy as np
import os


def set_global_seed(seed: int) -> NoReturn:
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)