# ML in prod
Production ready project to solve classification task from Kaggle Dataset "[Heart Disease Cleveland UCI](https://www.kaggle.com/datasets/cherngs/heart-disease-cleveland-uci)"

## Python version 
Python >= 3.6

## Installation
#### Install DvC
```bash
sudo snap install dvc --classic
```
#### Install Docker on Ubuntu 18.04
```bash
sudo apt install docker.io
```
#### Docker pull
```bash
docker pull xrenya/cont_app:latest
```

## Usage
#### Model pull using DvC
```bash
dvc pull
```

#### Docker run
```bash
docker run -p 1234:5000 --name cont_app app
```
### Tests
```bash
python -m pytest tests/test_app.py 
```
### GUI for application
```bash
PORT = 5000 local port, 1234 docker contrainer port, unless specified differently as stated above
http://0.0.0.0:PORT
```
### Inference conmmand
Example:
```bash
PORT = 5000 local port, 1234 docker contrainer port, unless specified differently as stated above

Healt status:
curl -X 'GET' \
  'http://0.0.0.0:PORT/health' \
  -H 'accept: application/json'
  
Predict:
curl -X 'GET' \
  'http://0.0.0.0:PORT/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "data":[
    [65.0, 1.0, 0.0, 138.0, 282.0, 1.0, 2.0, 174.0, 0.0, 1.4, 1.0, 1.0, 0.0] # your data
  ],
  "feature_names": [
    "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"
  ] # your columns names according to data above
}'
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
    ├── online_inference            <- Source code for use in this project.
    │   ├── config                  <- Config files
    │   │   ├── base_config.py          
    │   │   ├── config.py      
    │   │   └── logger.yaml
    │   │ 
    │   ├── model                   <- Folder for models
    │   │   ├── model.pkl
    │   │   └── transformer.pkl
    │   │
    │   ├── notebooks               <- Main codebase
    │   │   ├── heart_cleveland_upload.csv       <- Dataset
    │   │   └── model.ipynb         <- Notebook to save model/transfomer
    │   │
    │   └── src               <- Main codebase
    │       ├── utils.py       <- Utils function
    │
    ├── app.py                      <- Run an application
    ├── Dockerfile                  <- Docker configuration file
    └── requirements.txt            <- Requirement to install for application to run
