FROM python:latest

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip3 install ./requirements.txt

COPY . .

CMD ["python","main.py"]