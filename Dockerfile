# Python server's Dockerfile

FROM python:3.11.2
ENV PYTHONUNBUFFERED 1

RUN mkdir /python_assignment
WORKDIR /python_assignment
COPY . /python_assignment
RUN pip install -r requirements.txt
