FROM python:3.7-alpine

# Default to client flow if none specified
ENV FLOW=client

COPY requirements.txt /

RUN pip3 install -r /requirements.txt

EXPOSE 5000

COPY . /src

CMD cd /src/$FLOW && flask run --host=0.0.0.0