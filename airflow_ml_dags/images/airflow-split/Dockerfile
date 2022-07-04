FROM python:3.7-slim-stretch

COPY requirements.txt /requirements.txt
COPY split.py /split.py

RUN pip install -r /requirements.txt
ENTRYPOINT ["python", "split.py"]