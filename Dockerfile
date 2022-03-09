#Grab the latest ubuntu image
FROM ubuntu:latest

# Install python and pip
RUN apt update -y && apt install -y --no-install-recommends software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa

RUN apt install -y python3.9 python3.9-distutils curl
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.9 get-pip.py
RUN python3.9 -m pip install pipenv
#ADD ./src/requirements.txt /tmp/requirements.txt

# Install dependencies
#ADD Pipfile.lock Pipfile /opt/webapp/
#RUN pip3 install --no-cache-dir -q -r /tmp/requirements.txt
#ADD dkr_setup/setup.py pyproject.toml /opt/

# Run the image as a non-root user
RUN adduser --disabled-password myuser
USER myuser

# Add our code
ADD . /home/myuser
WORKDIR /home/myuser
RUN PIPENV_VENV_IN_PROJECT=1 python3.9 -m pipenv install --deploy --ignore-pipfile #--system
#RUN python3.9 -m pip list install -e . # looks like chloe was right after all
ENV PATH="/.venv/bin:$PATH"
ENV PORT=8080

#ENV PYTHONPATH=/opt/

#RUN pip3 install -e /opt/ && pip3 list

#RUN python3 --version

# Expose is NOT supported by Heroku
# EXPOSE 5000
# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku
#CMD gunicorn -w 4 --bind 0.0.0.0:80 wsgi
WORKDIR /home/myuser/src/webapp/
CMD python3.9 -m pipenv run gunicorn -w 4 --bind 0.0.0.0:$PORT wsgi