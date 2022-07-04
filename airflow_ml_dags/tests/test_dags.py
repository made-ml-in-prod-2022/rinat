import pytest
from airflow.models import DagBag


@pytest.fixture()
def dag_bag():
    return DagBag(dag_folder="dags/", include_examples=False)


def test_dag_imports(dag_bag):
    assert dag_bag.dags is not None
    assert dag_bag.import_errors == {}


def test_generate_data_dag_loaded(dag_bag):
    # from pdb import set_trace; set_trace()
    assert "1_generate_data" in dag_bag.dags
    assert len(dag_bag.dags["1_generate_data"].tasks) == 1


def test_train_pipeline_dag_loaded(dag_bag):
    # from pdb import set_trace; set_trace()
    assert "2_train_pipeline" in dag_bag.dags
    assert len(dag_bag.dags["2_train_pipeline"].tasks) == 5


def test_inference_dag_loaded(dag_bag):
    # from pdb import set_trace; set_trace()
    assert "3_inference" in dag_bag.dags
    assert len(dag_bag.dags["3_inference"].tasks) == 2


@pytest.mark.parametrize(
    "dag_id,tasks",
    [
        ("1_generate_data", ["docker-airflow-download"]),
        ("2_train_pipeline", ['await-data', 'split-data', 'preprocess-data', 'model-train', 'model-evaluation']),
        ("3_inference", ['await-data', 'generate-predicts'])
    ]
)
def test_dags_tasks(dag_bag, dag_id, tasks):
    # from pdb import set_trace;
    # set_trace()
    dag = dag_bag.dags[dag_id]
    for task, _ in list(dag.task_dict.items()):
        assert task in tasks
