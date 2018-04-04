export AIRFLOW_HOME=$(pwd)
export APP=COLORADO
export GOOGLE_CLIENT_ID=''
export GOOGLE_CLIENT_SECRET=''
python config/configure_airflow.cfg.py
python config/customize_dashboard.dev.py
airflow initdb
airflow webserver -d
airflow scheduler
