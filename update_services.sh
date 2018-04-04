docker-compose stop
docker-compose rm -f
docker-compose up --build -d
docker-compose exec web airflow scheduler
