# vgifify
Веб-сервис для создания gif'ки из видеофайла.
## Для разработчика
### Подготовка среды
* Форкнуть репозиторий к себе
* Склонировать форк и перейти в папку с ним
* Установить redis: `sudo apt-get install redis`
* Сделать virtualenv с python3: `virtualenv --python="$(which python3)" venv`
* Активировать virtualenv: `source venv/bin/activate`
* Загрузить зависимости: `pip install -r requirements.txt`
* Перейти в папку `src`
* Создать бд: `./manage.py migrate`

### Запуск dev сервера
* Запустить redis
* `./manage.py runserver` -- web-сервер
* `./manage.py rqworker` -- worker
