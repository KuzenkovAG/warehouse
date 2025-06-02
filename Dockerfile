# We use the official image of Python 3.12 based on Alpine Linux
FROM dts.ickamaz.ru/infra/python:3.12-alpine

# Set an environment variable to disable Python output buffering
ENV PYTHONUNBUFFERED=1

# Define arguments for authentication in PyPI and Nexus
ARG PYPI_USERNAME
ARG PYPI_PASSWORD
ARG NEXUS_HOST
ARG NEXUS_PYPI_USER
ARG NEXUS_PYPI_PASSWORD

# Set these arguments as environment variables
ENV PYPI_USERNAME=$PYPI_USERNAME \
    PYPI_PASSWORD=$PYPI_PASSWORD \
    NEXUS_HOST=$NEXUS_HOST \
    NEXUS_PYPI_USER=$NEXUS_PYPI_USER \
    NEXUS_PYPI_PASSWORD=$NEXUS_PYPI_PASSWORD

# Define arguments for GitLab CI
ARG GITLAB_CI_PROJECT_ID
ARG GITLAB_CI_PROJECT_URL
ARG GITLAB_CI_PROJECT_TITLE
ARG GITLAB_CI_PIPELINE_ID
ARG GITLAB_CI_PIPELINE_URL
ARG GITLAB_CI_COMMIT_TAG
ENV CI_PROJECT_ID=$GITLAB_CI_PROJECT_ID \
    CI_PROJECT_URL=$GITLAB_CI_PROJECT_URL \
    CI_PROJECT_TITLE=$GITLAB_CI_PROJECT_TITLE \
    CI_PIPELINE_ID=$GITLAB_CI_PIPELINE_ID \
    CI_PIPELINE_URL=$GITLAB_CI_PIPELINE_URL \
    CI_COMMIT_TAG=$GITLAB_CI_COMMIT_TAG

# Update the system and install the necessary dependencies
RUN apk update && apk add --no-cache \
    build-base \
    python3-dev \
    yaml-dev \
    bash \
    dos2unix \
    busybox=1.36.1-r29 \
    libcrypto3 \
    proj \
    proj-dev \
    proj-util

# Update pip, setuptools and wheel
RUN pip install --upgrade pip setuptools wheel

# Install Cython globally
RUN pip install cython

# Install pipenv
RUN pip install pipenv==2023.12.1

# Copy the source code and configuration files to the working directory of the container
COPY src /opt/app/
COPY docker-entrypoint.sh /opt/app/
COPY Pipfile /opt/app/
COPY Pipfile.lock /opt/app/
COPY mypy.ini /opt/app/
COPY ruff.toml /opt/app/
COPY pytest.ini /opt/app/
COPY coverage.ini /opt/app/

# Set the working directory
WORKDIR /opt/app/

# Install project dependencies
RUN pipenv install --ignore-pipfile

# Convert the docker-entrypoint.sh format and make it executable
RUN dos2unix /opt/app/docker-entrypoint.sh && chmod +x /opt/app/docker-entrypoint.sh

# Define the entry point for the container
ENTRYPOINT ["/opt/app/docker-entrypoint.sh"]

# Default command to start an application
CMD [ "ls", "-l" ]
