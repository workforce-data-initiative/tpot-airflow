# Helper functions to create airflow user

check_user_exists() {
    echo $(id -u $1 > /dev/null 2>&1; echo $?)
}

delete_airflow_user() {
    userdel --force --remove {{cfg.superuser.name}}
}

create_airflow_user() {
    if [ $(check_user_exists "{{cfg.superuser.name}}") -eq 1 ]; then
        echo "Creating airflow superuser"
        useradd --user-group {{cfg.superuser.name}}
    fi

    echo "User-$(id {{cfg.superuser.name}})"
}
