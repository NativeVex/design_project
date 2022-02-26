#Grab the latest alpine image
FROM ubuntu:latest

# Install python and pip
RUN apt update -y && apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3.9 python3-pip
ADD ./webapp/requirements.txt /tmp/requirements.txt
ADD Pipfile.lock Pipfile /opt/webapp/

# Install dependencies
RUN pip3 install --no-cache-dir -q -r /tmp/requirements.txt

# Add our code
ADD ./webapp /opt/webapp/
WORKDIR /opt/webapp

RUN python3 --version

# Expose is NOT supported by Heroku
# EXPOSE 5000

# Run the image as a non-root user
RUN adduser --disabled-password myuser
USER myuser

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku
#CMD gunicorn -w 4 --bind 0.0.0.0:80 wsgi
CMD gunicorn -w 4 --bind 0.0.0.0:$PORT wsgi
