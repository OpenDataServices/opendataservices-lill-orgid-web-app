# LILL Org-id - Web app


To set up app add env vars:

* AZURE_POSTGRES_CONNECTION_STRING - postgres database connection string

Dev with docker
===============

Create `.env` with settings:

    AZURE_POSTGRES_CONNECTION_STRING=postgres://lillorgid:xxxxxxxxxxxxxxxxxxx@xxxxxxxxxxxxxxxxxx.postgres.database.azure.com/xxxxxxxxxxxxxxxxxxx?sslmode=require

Docker is used in production, so sometimes you may want to run locally with Docker to debug issues:

    docker compose -f docker-compose.dev.yml down # (if running)
    docker compose -f docker-compose.dev.yml build --no-cache
    docker compose -f docker-compose.dev.yml up # (to restart)

Run commands:

    docker compose -f docker-compose.dev.yml run iati-cove-app-dev python manage.py migrate
    docker compose -f docker-compose.dev.yml run iati-cove-app-dev python manage.py collectstatic --noinput

