FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

RUN apt-get update
RUN apt-get install python3 python3-pip -y
RUN pip3 install --upgrade pip

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt
COPY ./app /app

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]