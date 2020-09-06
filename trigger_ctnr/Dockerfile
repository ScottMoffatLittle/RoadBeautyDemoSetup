FROM python:3.6-slim

#RUN apt-get update && apt-get upgrade -y && apt-get install -y \
#  apt-utils \
#  nano \
#  curl \
#  wget \
#  htop \
#  nmon \
#  vim \
#  httpie \
#  && apt-get clean -y

RUN mkdir /opt/gpudb
RUN mkdir /opt/gpudb/kml
RUN mkdir /opt/gpudb/kml/trigger
WORKDIR /opt/gpudb/kml/trigger

RUN pip install --no-cache-dir gpudb

ADD ./trigger_model.py ./
ADD ./trigger_model.sh ./

RUN ["chmod", "+x",  "trigger_model.sh"]

ENTRYPOINT ["/opt/gpudb/kml/trigger/trigger_model.sh"]
