export AIRFLOW_HOME=$(pwd)
airflow initdb
python remove_airflow_examples.py
airflow resetdb -y
python customize_dashboard.dev.py
airflow webserver
