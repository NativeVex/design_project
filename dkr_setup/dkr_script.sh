#!/bin/sh
su postgres -c "whoami"
su postgres -c "/usr/lib/postgresql/12/bin/postgres -D /var/lib/postgresql/12/main -c config_file=/etc/postgresql/12/main/postgresql.conf &"
su myuser -c "gunicorn -w 4 --bind 0.0.0.0:80 wsgi"
