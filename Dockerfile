# Use the official Python image from the DockerHub
FROM ubuntu:20.04

# Set the working directory in docker
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .


# Install Python 3.9 and pip
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.9 python3.9-distutils && \
    apt-get install -y python3-pip

# Make Python 3.9 as the default python3 version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 2

# Upgrade pip and install the required packages
RUN python3 -m pip install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt


# Copy the content of the local src directory to the working directory
COPY . .

# Specify the command to run on container start
CMD [ "python3", "./main.py" ]
