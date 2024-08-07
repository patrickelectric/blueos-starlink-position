FROM python:3.11-slim

COPY app /app
RUN python -m pip install /app --extra-index-url https://www.piwheels.org/simple


LABEL version="v0.0.5"

ARG IMAGE_NAME

LABEL permissions='\
{\
  "NetworkMode": "host",\
  "HostConfig": {\
    "Privileged": true,\
    "NetworkMode": "host"\
  }\
}'

ARG AUTHOR
ARG AUTHOR_EMAIL
LABEL authors='[\
    {\
        "name": "Patrick J. Pereira",\
        "email": "patrickelectric@gmail.com"\
    }\
]'

ARG MAINTAINER
ARG MAINTAINER_EMAIL
LABEL company='{\
        "about": "",\
        "name": "Patrick J. Pereira",\
        "email": "patrickelectric@gmail.com"\
    }'
LABEL type="tool"
ARG REPO
ARG OWNER
LABEL readme='https://raw.githubusercontent.com/patrickelectric/blueos-starlink-position/{tag}/README.md'
LABEL links='{\
        "source": "https://github.com/patrickelectric/blueos-starlink-position"\
    }'
LABEL requirements="core >= 1.1"

ENTRYPOINT cd app && python main.py
