FROM python:3.10

COPY . .

RUN apt-get update && apt-get install libgl1

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "app.py"]
