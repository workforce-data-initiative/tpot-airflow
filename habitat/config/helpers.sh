# Helper functions to create airflow user

check_user_exists() {
    echo $(id -u $1 > /dev/null 2>&1; echo $?)
}

delete_db_superuser() {
    userdel --force --remove {{cfg.superuser.name}}
}

create_db_superuser() {
    if [ $(check_user_exists "{{cfg.superuser.name}}") -eq 1 ]; then
        echo "Create airflow superuser"
        useradd --user-group --create-home {{cfg.superuser.name}}
    fi

    echo "User-$(id {{cfg.superuser.name}})"
}
