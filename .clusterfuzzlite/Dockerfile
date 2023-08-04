FROM gcr.io/oss-fuzz-base/base-builder-python:v1

RUN apt-get update && apt-get install -y make autoconf automake libtool

COPY . $SRC/cronk
WORKDIR cronk
COPY .clusterfuzzlite/build.sh .clusterfuzzlite/*.dict $SRC/

RUN pip3 install hypothesis --upgrade
