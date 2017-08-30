heroku container:login
if [ $CIRCLE_BRANCH = 'master' ]; then heroku git:remote -a tpot-airflow; fi
if [ $CIRCLE_BRANCH = 'develop' ]; then heroku git:remote -a tpot-airflow-dev; fi
heroku container:push web
