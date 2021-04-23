FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /cardopt

COPY requirements.txt /cardopt/requirements.txt

RUN pip install -r requirements.txt

COPY . /cardopt

CMD python manage.py runserver 0.0.0.0:8000
