# AskMe
программа для организации и поддержки форума

### Установка программы
`git clone https://github.com/Sergei39/TP-WEB-semestr1.git` \
`cd askme`

### Config
файл конфиг лежит `askme/.env-admin.prod`

### Создание или запуск форума:
`./command/start` \
форум запустится на 5001 порту

### Остановка форума:
`./command/stop`

### Создание модератора
`./command/create_user` \
path для входа в админку `/admin`


### Генерация случайных данных для наполнения форума
`docker-compose exec web_1 ./manage.py generate_data --db_size small`