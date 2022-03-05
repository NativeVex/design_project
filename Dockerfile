################################
#POSTGRES CODE STOLEN FROM https://docs.docker.com/samples/postgresql_service/
#TODO: Make the password a GH secret (or other form of secret)
#      Make this code either always install PG12 or not depend on it being version 12
# Command to run POSTGRES:
#/usr/lib/postgresql/12/bin/postgres -D /var/lib/postgresql/12/main -c config_file=/etc/postgresql/12/main/postgresql.conf &
# I added this in dkr_setup/dkr_script.sh. Problem is this command needs to be run as the postgres user and I don't know
# if I wanna have gunicorn running as postgres or try to get postgres setup to run under myuser.
################################
#Grab the latest ubuntu image
FROM ubuntu:latest

# Install python and pip
RUN apt update -y && apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3.9 python3-pip postgresql postgresql-client postgresql-contrib
ADD ./src/requirements.txt /tmp/requirements.txt

#Add Postgres PGP key

#Add Postgres Repo

################################
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

RUN adduser --disabled-password myuser
USER postgres
RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER myuser WITH SUPERUSER PASSWORD 'docker';" &&\
    createdb -O myuser docker
RUN echo "host all all 0.0.0.0/0 md5" >> /etc/postgresql/12/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/12/main/postgresql.conf
#TODO: change the passwords on this to be secret somehow
#EXPOSE not supported by Heroku so we have to change here
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

USER myuser

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku
CMD gunicorn -w 4 --bind 0.0.0.0:80 wsgi
#CMD gunicorn -w 4 --bind 0.0.0.0:$PORT wsgi
