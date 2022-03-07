#Grab the latest alpine image
FROM ubuntu:latest

# Install python and pip
RUN apt update -y && apt install -y --no-install-recommends software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3.9 python3-pip
RUN pip install pipenv
#ADD ./src/requirements.txt /tmp/requirements.txt

# Install dependencies
#ADD Pipfile.lock Pipfile /opt/webapp/
#RUN pip3 install --no-cache-dir -q -r /tmp/requirements.txt
#ADD dkr_setup/setup.py pyproject.toml /opt/

# Add our code
ADD . /opt/webapp/
WORKDIR /opt/webapp/
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --system --deploy --ignore-pipfile
ENV PATH="/.venv/bin:$PATH"
ENV PORT=8080

#ENV PYTHONPATH=/opt/

#RUN pip3 install -e /opt/ && pip3 list

#RUN python3 --version

# Expose is NOT supported by Heroku
# EXPOSE 5000

# Run the image as a non-root user
RUN adduser --disabled-password myuser
USER myuser

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku
#CMD gunicorn -w 4 --bind 0.0.0.0:80 wsgi
CMD gunicorn -w 4 --bind 0.0.0.0:$PORT app
