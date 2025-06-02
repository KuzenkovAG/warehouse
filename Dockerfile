# We use the official image of Python 3.12 based on Alpine Linux
FROM python:3.12-alpine

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
