## Airflow

### Docker installation
```
sudo install docker
```

## Usage

### Prepare local storage in `dags/utils.py`
Example:
```
DEFAULT_VOLUME: "/home/user/Documents/MADE/MLProd/airflow/test/data:/data"
```
`/home/user/Documents/MADE/MLProd/airflow/test/data` - directory on local machine

To store output from Docker Containers

### Docker compose
```
sudo docker-compose up --build
```
### Test DAGS
`python -m pytest -v`  
I had a problem with airflow pytest due to different versions, so I just removed `volume` in DAG to run pytest. 

