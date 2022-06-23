# ML in prod
Production ready project to solve classification task from Kaggle Dataset "[Heart Disease Cleveland UCI](https://www.kaggle.com/datasets/cherngs/heart-disease-cleveland-uci)"

## Python version 
Python >= 3.6

## Installation
#### Pyenv
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
#### Conda
```bash
conda create -n venv python=3.6 anaconda
source activate venv
conda install --file requirements.txt
```

## Usage
### Train
```bash
python ml_project/train.py
```
Also you can change configurations when run the script. For example:
```bash
python train.py pipeline=custom_pipeline.yaml
python train.py checkpoint_file=/home/username/location_to_save_model/
```
Or use multirun option:
```bash
python train.py --multirun pipeline=custom_pipeline.yaml,pipeline.yaml
python train.py --multirun metrics=f1.yaml,roc_auc.yaml,accuracy.yaml
```
Logger's output
```bash
2022/05/09 18:24:08 INFO mlflow.tracking.fluent: Experiment with name 'Classification' does not exist. Creating a new experiment.
[2022-24-05/09/22 18:24:08] [root] [INFO] [MlFlow] logging initiated successfully.
[2022-24-05/09/22 18:24:08] [predictor.engine.trainer] [INFO] The global random seed is fixed 3407
[2022-24-05/09/22 18:24:08] [predictor.data.data] [INFO] Initializing data preprocessing}
[2022-24-05/09/22 18:24:08] [predictor.data.data] [INFO] Reading data from /home/user/MLProd/rinat/ml_project/data/heart_cleveland_upload.csv
[2022-24-05/09/22 18:24:08] [predictor.data.data] [INFO] Split dataset into train/test sizes: 0.8/0.2
[2022-24-05/09/22 18:24:08] [predictor.pipeline.pipeline] [INFO] The model is initialized
[2022-24-05/09/22 18:24:08] [predictor.engine.trainer] [INFO] Model fitting
[2022-24-05/09/22 18:24:08] [predictor.engine.trainer] [INFO] Model prediction on validation dataset
[2022-24-05/09/22 18:24:08] [predictor.engine.trainer] [INFO] roc_auc_score on validation dataset: 0.8481646273637374
[2022-24-05/09/22 18:24:08] [predictor.engine.trainer] [INFO] accuracy_score on validation dataset: 0.85
[2022-24-05/09/22 18:24:08] [predictor.engine.trainer] [INFO] f1_score on validation dataset: 0.8363636363636363
[2022-24-05/09/22 18:24:08] [predictor.engine.trainer] [INFO] Saving pipeline into /home/user/MLProd/rinat/ml_project/model_weights/LR.pkl
```
Results will be in ml_project/outputs/*starting date*/*starting time*

### Inference
```bash
python ml_project/predict.py 'checkpoint_file=full_path_to_the_checkpoint' \ 
    'csv_output=specified_output_dir csv_filename=output_csv_filename' 
```
Example:
```bash
python ml_project/predict.py \ 
    'checkpoint_file=/home/user/homework1/ml_project/LR.pkl' \ 
    'csv_filename=output.csv'
```
Project Organization
------------
    ├── LICENSE
    ├── README.md                   <- The top-level README for developers using this project.
    ├── data                        <- The data sets for modeling.
    ├── notebooks                   <- Jupyter notebooks
    ├── requirements.txt            <- The requirements file for reproducing the analysis environment, e.g.
    │                                   generated with `pip freeze > requirements.txt`
    ├── requirements-dev.txt        <- The requirements with packages for development & testing
    │
    ├── ml_project                  <- Source code for use in this project.
    │   ├── config                  <- Config files
    │   │   ├── data         
    │   │   ├── metrics    
    │   │   ├── pipeline           
    │   │   ├── train.yaml         
    │   │   ├── predict.yaml         
    │   │   └── logger.yaml
    │   │ 
    │   ├── data                    <- Folder for dataset
    │   │   └── heart_cleveland_upload.csv
    │   │
    │   ├── predictor               <- Main codebase
    │   │   ├── data     
    │   │   │    └── data.py    
    │   │   ├── engine     
    │   │   │    └── trainer.py   
    │   │   ├── metrics     
    │   │   │    └── metrics.py 
    │   │   ├── pipeline     
    │   │   │    └── pipeline.py        
    │   │   ├── models     
    │   │   │    └── models.py          
    │   │   └── utils     
    │   │        └── utils.py 
    │   │
    │   ├── entities                <- Dataclasses for config validation
    │   │   └── config.py
    │   │
    │   ├── train.py       <- Train pipeline main script
    │   └── predict.py   <- Inference pipeline main script
    │
    ├── tests                       <- Tests for pipelines and functions
    ├── setup.cfg                   <- Store pytest configurations
    └── setup.py                    <- Makes project pip installable (pip install -e .) so src can be imported
--------

### Config supports
The project supports DataClass as HydraConfig or just yaml config files.
