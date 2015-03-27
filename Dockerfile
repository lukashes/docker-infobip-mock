FROM ubuntu:14.04
MAINTAINER Yegor Lukash <yegor.lukash@gmail.com>

# Update the image
RUN apt-get update -y && apt-get upgrade -y

# Install Dependencies
RUN apt-get update -y --fix-missing
RUN apt-get install -y python-dev
RUN apt-get install -y python-pip
# RUN pip install --upgrade pip
RUN pip install Flask

# Sync code
RUN mkdir -p /www/infobip && cd /www/infobip
ADD . /www/infobip

# Run it!
ENTRYPOINT ["python", "/www/infobip/__init__.py"]

EXPOSE 5005 5005
