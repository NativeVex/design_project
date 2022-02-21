
FROM docker.io/python:3.8-slim AS builder
RUN pip install --user pipenv
# Tell pipenv to create venv in the current directory
ENV PIPENV_VENV_IN_PROJECT=1
# Pipefile contains flask
ADD Pipfile.lock Pipfile /app/
WORKDIR /app
# NOTE: If you install binary packages required for a python module, you need
# to install them again in the runtime. For example, if you need to install pycurl
# you need to have pycurl build dependencies libcurl4-gnutls-dev and libcurl3-gnutls
# In the runtime container you need only libcurl3-gnutls
# RUN apt install -y libcurl3-gnutls libcurl4-gnutls-dev
RUN /root/.local/bin/pipenv sync
RUN /app/.venv/bin/python -c "import flask; print(flask.__version__)"

FROM docker.io/python:3.8-slim AS runtime
RUN mkdir -v -p /app/venv
COPY --from=builder /app/.venv/ /app/venv/
RUN /app/venv/bin/python -c "import flask; print(flask.__version__)"

# HERE GOES ANY CODE YOU NEED TO ADD TO CREATE YOUR APPLICATION'S IMAGE
# For example
# RUN apt install -y libcurl3-gnutls
# RUN adduser --uid 123123 coolio
COPY . /app
WORKDIR /app/

CMD ["./venv/bin/python", "index.py"]
