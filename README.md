# API routes

- [x] locate any Vietnamese terms: show it's
    - [x] vn_main, en_main, vn_synonyms
    - [x] en_synonyms
    - [x] cui, doid
- [x] locate any English terms
    - [x] vn_main
    - [x] en_main
    - [x] vn_synonyms
    - [x] en_synonyms
    - [x] cui, doid

- [x] simply check if a vi/en name is registered: simply return True or False (helpful for data manual entry)

- [x] check if every English main is mapped to at least one standard (return True False; helpful for data health checking). Can also be implemented in Flask app

# Installation

1. Make sure you have `docker` and `docker-compose` installed

2. Create .env.dev file containing url to your database like this

```bash
DEV_DATABASE_URI="mssql+pyodbc://<you_user>:<your_password>@<your_database_host>:1433/<your_database_name>?autocommit=False&driver=ODBC+Driver+17+for+SQL+Server"
```

For example:
```bash
DEV_DATABASE_URI="mssql+pyodbc://tungdev:Tung1234@localhost:1433/dev_db?autocommit=False&driver=ODBC+Driver+17+for+SQL+Server"
```

3. Build the docker image

```bash
docker-compose build
```

then

```bash
docker-compose up
``

Wait till 'Uvicorn is running...' shows up, then go to your browser:
`localhost:8008/status/validate`. Check out other endpoints at 
`localhost:8008/docs`
