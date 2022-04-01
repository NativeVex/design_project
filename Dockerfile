#Grab the latest ubuntu image
FROM ubuntu:latest

# Install python and pip
RUN apt update && apt upgrade -y
RUN apt install -y --no-install-recommends software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt install -y python3.9 python3.9-distutils curl
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.9 get-pip.py
RUN python3.9 -m pip install pipenv
#ADD ./src/requirements.txt /tmp/requirements.txt

# Install dependencies
ADD Pipfile.lock Pipfile /opt/webapp/
#RUN pip3 install --no-cache-dir -q -r /tmp/requirements.txt
#ADD dkr_setup/setup.py pyproject.toml /opt/

# Run the image as a non-root user
RUN adduser --disabled-password myuser

# Add our code
ADD . /opt/
WORKDIR /opt/
#RUN python3.9 -m pip list install -e . # looks like chloe was right after all
#ENV PATH="/.venv/bin:$PATH"
ENV PORT=80

ENV PYTHONPATH=/opt/src/

#this line needs to make a dir in /opt/ and needs to be root for that
RUN python3.9 -m pipenv install -e /opt/

RUN PIPENV_VENV_IN_PROJECT=1 python3.9 -m pipenv install --deploy --ignore-pipfile 
# --system
#RUN python3 --version

# Expose is NOT supported by Heroku
# EXPOSE 5000

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku
#CMD gunicorn -w 4 --bind 0.0.0.0:80 wsgi
USER myuser
WORKDIR /opt/src/webapp
CMD /opt/.venv/bin/gunicorn -w 1 --bind 0.0.0.0:$PORT wsgi
