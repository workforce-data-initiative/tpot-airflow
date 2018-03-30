export AIRFLOW_HOME=$(pwd)
airflow initdb
python config/remove_airflow_examples.py
airflow resetdb -y
python config/customize_dashboard.dev.py
airflow webserver -d
airflow scheduler
