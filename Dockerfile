#Grab the latest ubuntu image
FROM ubuntu:latest

# Install python and pip
RUN apt update -y && apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3.9 python3-pip
ADD ./src/requirements.txt /tmp/requirements.txt

# Install dependencies
ADD Pipfile.lock Pipfile /opt/webapp/
RUN pip3 install --no-cache-dir -q -r /tmp/requirements.txt
ADD dkr_setup/setup.py pyproject.toml /opt/

# Add our code
ADD ./src/webapp /opt/webapp/
WORKDIR /opt/webapp/

ENV PYTHONPATH=/opt/

RUN pip3 install -e /opt/ && pip3 list

RUN python3 --version

# Expose is NOT supported by Heroku
# EXPOSE 5000

# Run the image as a non-root user
RUN adduser --disabled-password myuser
USER myuser

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku
CMD gunicorn -w 4 --bind 0.0.0.0:80 wsgi
#CMD gunicorn -w 4 --bind 0.0.0.0:$PORT wsgi
