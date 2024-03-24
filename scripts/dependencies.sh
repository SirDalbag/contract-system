execute_command() {
    eval "$1"
    if [ $? -eq 0 ]; then
        echo -e "\e[94m$1 success!\e[0m"
    else
        echo -e "\e[91mError: $1\e[0m"
    fi
}

execute_command "cd /var/www/contracts/contract_system_main/frontend && npm i"
execute_command "cd /var/www/contracts/contract_system_main/frontend && npm run build"
execute_command "cd /var/www/contracts/contract_system_main/backend/django && python3.11 -m venv venv"
execute_command "cd /var/www/contracts/contract_system_main/backend/django && source venv/bin/activate && pip install -r requirements-prod.txt && python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py createsuperuser"
