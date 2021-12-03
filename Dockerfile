FROM python:latest
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
RUN apt-get update


COPY requirements.txt /code
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt
COPY . /code/
WORKDIR code/Ecom-Shop-main
CMD python3 manage.py makemigrations
CMD python3 manage.py migrate
CMD gunicorn shop.wsgi:application --bind 0.0.0.0:8000
