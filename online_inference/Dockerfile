FROM python:3.8
RUN python -m venv venv
RUN . venv/bin/activate \
 && pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
RUN pip

RUN mkdir /app

COPY src app/src
COPY model app/model
COPY config app/config
COPY app.py app/app.py

WORKDIR /app

RUN dvc pull

EXPOSE 5000

CMD ["python", "app.py"]
