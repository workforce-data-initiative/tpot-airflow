# tpot-airflow

Orchestration of data processing tasks to power the reporting TPOT ETP API

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3](https://pyup.io/repos/github/workforce-data-initiative/tpot-airflow/python-3-shield.svg)](https://pyup.io/repos/github/workforce-data-initiative/tpot-airflow/)
[![Updates](https://pyup.io/repos/github/workforce-data-initiative/tpot-airflow/shield.svg)](https://pyup.io/repos/github/workforce-data-initiative/tpot-airflow/)


Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Support](#support)
- [Contributing](#contributing)

## Installation

Clone the project and cd into the folder.
```bash
git clone https://github.com/workforce-data-initiative/tpot-airflow.git && cd tpot-airflow
```

Install requirements (preferably in a virtual environment)

```bash
pip install -r requirements.txt
```

Note that the project is using Python 3.6.2 in development

## Usage

Initialize the meta database by running:
```bash
airflow initdb
```

Start the airflow webserver and expolre the UI at [localhost:8080](http://localhost:8080).
```bash
airflow runserver
```
Note that you have optional arguments:

- `-p=8080, --port=8080` to specify which port to run the server
- `-w=4, --workers=4` to specify the number of workers to run the webserver on


#### Aside

You can customize the dashboard to read *TPOT - Airflow* instead of *Airflow* by running `python customize_dashboard.py`

## Support

Please confirm if [the issue has not been raised](https://github.com/workforce-data-initiative/tpot-airflow/issues/new) then you can open an issue for support.

## Contributing

Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/workforce-data-initiative/tpot-airflow/compare).
