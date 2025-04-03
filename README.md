# funtech order app


## Run

Нужен установленный [docker](https://docs.docker.com/engine/install/)


### Заполняем енвы
Можно ничего там не менять

```bash
cp .env.example .env
```

### Билдим и запускаем всю инфраструктуру
```bash
make run_dev
```

### Накатываем миграции в базу
```bash
make upgrade
```

Приложение доступно на `localhost:8000`

Swagger доступен на `localhost:8000/docs`
