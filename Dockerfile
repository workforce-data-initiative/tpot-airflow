# Set python:3 as Base image
FROM python:3

# Set the working directory for RUN, CMD, ENTRYPOINT, COPY and ADD
WORKDIR /usr/src/app

# Copy requirements.txt to a path relative to WORKDIR
COPY requirements.txt ./

# Install dependencies
RUN pip install -r requirements.txt

# Copy the other files to a path relative to WORKDIR
COPY . .

# Run the following commands
ENV AIRFLOW_HOME=/usr/src/app
ENV APP=COLORADO
ARG GOOGLE_CLIENT_ID
ARG GOOGLE_CLIENT_SECRET
RUN python config/configure_airflow.cfg.py && python config/customize_dashboard.py
RUN airflow initdb

# Set command to run as soon as container is up
CMD airflow webserver -p=$PORT
