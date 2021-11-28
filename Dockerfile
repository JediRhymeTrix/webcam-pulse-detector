FROM python:3.10

RUN pip install -r /deploy/app/requirements.txt

ENTRYPOINT ["python", "app.py"]