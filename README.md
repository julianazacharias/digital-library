# Digital Library

A simple API buildt with FastAPI Sync to manage books.
This API allows users to perform operations such as adding, updating, and retrieving books.

## How to run the project

### Requirements

- [Python](https://www.python.org/) ^3.12

### With poetry

1. Install the dependencies:

```bash
poetry install
```

2. Activate the virtual environment:

```bash
poetry shell
```

3. Run the application:

```bash
task run
```

4. Run the tests:

```bash
task test
```

### With Docker

1. Build the image:

```bash
docker-compose build
```

2. Run the application:

```bash
docker-compose up
```

### .ENV file:

Insert your API KEY value on **.env** file:

- DATABASE_URL=""
- SECRET_KEY=""
- ALGORITHM=""
- ACCESS_TOKEN_EXPIRE_MINUTES=30

## Everything used in this project

- [Python 3.12](https://www.python.org/)
- [Poetry](https://python-poetry.org/) to manage dependencies.
- [FastAPI](https://fastapi.tiangolo.com/) as the framework
- [SQLAlchemy](https://www.sqlalchemy.org/) for database management.
- [Pydantic](https://pydantic-docs.helpmanual.io/) for validating and converting Data-Transfer-Objects and database models.
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) for database migrations.
- [PostgreSQL](https://www.postgresql.org/) as the database.
- [JWT](https://jwt.io/) for handling authorization.
- [Docker](https://www.docker.com/) for containerization.
- [Docker Compose](https://docs.docker.com/compose/) for managing containers.

## Credits

Special thanks to the [FastAPI do Zero](https://fastapidozero.dunossauro.com/) course. You can find the project requirements [here](https://fastapidozero.dunossauro.com/14/#o-projeto).
