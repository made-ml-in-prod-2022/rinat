import json
import os
from dataclasses import asdict, dataclass, field


@dataclass
class Config:
    logger: str = "config/logger.yaml"
    checkpoint_file: str = "model/model.pkl"
    def to_dict(self) -> dict:
        res = {}
        for k, v in asdict(self).items():
            try:
                if isinstance(v, dict):  # noqa: WPS220
                    res[k] = json.dumps(v, indent=4)
                else:
                    res[k] = str(v)
            except Exception:
                res[k] = str(v)
        return res