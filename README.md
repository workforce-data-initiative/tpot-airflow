# tpot-airflow

Orchestration of data processing tasks to power the reporting TPOT ETP API

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3](https://pyup.io/repos/github/workforce-data-initiative/tpot-airflow/python-3-shield.svg)](https://pyup.io/repos/github/workforce-data-initiative/tpot-airflow/)
[![Updates](https://pyup.io/repos/github/workforce-data-initiative/tpot-airflow/shield.svg)](https://pyup.io/repos/github/workforce-data-initiative/tpot-airflow/)
[![CircleCI](https://circleci.com/gh/workforce-data-initiative/tpot-airflow.svg?style=svg)](https://circleci.com/gh/workforce-data-initiative/tpot-airflow)


Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [Support](#support)
- [Contributing](#contributing)

## DAGS

Before you go very far, note that you'll need to enter 3 key values into the file [dags/programs_registry_db_link.py](dags/programs_registry_db_link.py) for now:
- `aws_access_key_id` in line 33 of [dags/programs_registry_db_link.py](dags/programs_registry_db_link.py#L33)
- `aws_secret_access_key` in line 34 of [dags/programs_registry_db_link.py](dags/programs_registry_db_link.py#L34)
- `DB` in line 42 of [dags/programs_registry_db_link.py](dags/programs_registry_db_link.py#L42)

Only `programs_registry_db_link` DAG is fully functional.

## Installation

1. Clone the project and cd into the folder.

    ```bash
    git clone https://github.com/workforce-data-initiative/tpot-airflow.git && cd tpot-airflow
    ```

    If you have a Google Console project for OAuth 2.0, run the webserver and scheduler in that same container:

    ```bash
    export GOOGLE_CLIENT_ID=...
    export GOOGLE_CLIENT_SECRET=...
    docker-compose up -d
    docker-compose exec web airflow scheduler
    ```

    To test it out real quick using Docker just change line `179` in [airflow.cfg](airflow.cfg#L179) and change it to *authenticate = False* then run the webserver and scheduler in that same container:

    ```bash
    docker-compose up -d
    docker-compose exec web airflow scheduler
    ```

    and explore the UI at [localhost:8080](http://localhost:8080).

2. Install requirements (preferably in a virtual environment)
    ```bash
    pip install -r requirements.txt
    ```
    Note that the project is using Python 3.6.2 in development

3. Prepare the home for `airflow`:
    ```bash
    export AIRFLOW_HOME=$(pwd)
    export GOOGLE_CLIENT_ID=... (optional as long as you edited airflow.cfg)
    export GOOGLE_CLIENT_SECRET=... (optional as long as you edited airflow.cfg)
    ```

## Usage

Follow through steps 1 to 3:

_Running `sh setup.sh` is step 1, 2 and 3 in a single script_. Then get to [localhost:8080](http://localhost:8080).

1. Setup airflow:
    ```bash
    python config/remove_airflow_examples.py
    airflow resetdb -y
    export APP=TPOT [or some other name] (Optional)
    python config/customize_dashboard.dev.py (Optional)
    ```

  Running `python customize_dashboard.dev.py` customizes the dashboard to read *TPOT - Airflow* instead of *Airflow*  

2. Initialize the meta database by running:
    ```bash
    airflow initdb
    ```

3. Start the airflow webserver and explore the UI at [localhost:8080](http://localhost:8080).
    ```bash
    airflow webserver
    ```
Note that you have optional arguments:

- `-p=8080, --port=8080` to specify which port to run the server
- `-w=4, --workers=4` to specify the number of workers to run the webserver on


## Deployment
#### Docker

RUN `docker build -t tpot-airflow -f Dockerfile.dev .`

#### Heroku

RUN `sh heroku.sh`

#### AWS EC2
1. Setup an EC2 instance in AWS (ensure that you download the `.pem` file)
2. Authorise inbound traffic for this instance by adding a rule to the security group to accept traffic on port `8080` (explained [here](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/authorizing-access-to-an-instance.html))
3. Connect to the instance via `ssh` (explained [here](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html)).

    Run the following:
    - `sudo yum install git`
    - `git clone https://github.com/workforce-data-initiative/tpot-airflow.git`
    - `cd tpot-airflow`
    - `sh aws_setup.sh`
    - `sh docker_setup.sh`
    - `logout` - then ssh into the container again to pick up the new docker group permissions
    - `tmux`
    - `docker-compose up -d`

    It is advised that the codebase is modified in Github. Pull any update done to the codebase by running:
    - `git pull origin master` - or the relevant branch

For you to ssh into an already running instance, ask for the `.pem` and run:

```bash
ssh -i "<>.pem" ec2-user@<Public DNS>
```

For example: `ssh -i "airflow.pem" ec2-user@random.compute-1.amazonaws.com`

You'll need to ssh to setup `keys` intentionally not included on the codebase.
## Support

Please confirm if [the issue has not been raised](https://github.com/workforce-data-initiative/tpot-airflow/issues/new) then you can open an issue for support.

## Contributing

Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/workforce-data-initiative/tpot-airflow/compare).
