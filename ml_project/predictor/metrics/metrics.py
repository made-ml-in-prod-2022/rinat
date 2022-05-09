from sklearn.metrics import roc_auc_score, accuracy_score, f1_score


def roc_auc_metric():
    return {
        "roc_auc_score": roc_auc_score,
    }


def accuracy_metric():
    return {
        "accuracy_score": accuracy_score,
    }


def f1_metric():
    return {
        "f1_score": f1_score,
    }


def metrics():
    return {
        "roc_auc_score": roc_auc_score,
        "accuracy_score": accuracy_score,
        "f1_score": f1_score
    }
