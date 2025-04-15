Сервис note_book для записи контактов. Приложение будет доступно по адресу http://127.0.0.1:7001 (по умолчанию)


#### BUILD
`sh build.sh`

#### RUN
`sh run.sh`

Переменные окружения, которые можно передать в run файле:
- **APP_HOST** - хост приложения (по умолчанию '0.0.0.0')
- **APP_PORT** - порт приложения (по умолчанию 7001)
- **CONFIG_FILE** - расположение файла конфигурации. (Конфиг следует прокинуть в контейнер через volume)

## SETUP
#### CONFIG

Для конфигурации приложения используется YAML-файл, содержащий следующие настройки:
 - **db** - секция, описывающая настройки базы данных
   - **db_name** - название базы данных
   - **table_name** - название таблицы для хранения данных

