FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

# Install requirements
ADD requirements.txt /code/
RUN pip install -r requirements.txt


ADD . /code/
# We will specify the CMD in docker-compose.yaml