# FastAPI with Django ORM

This is a template repository for FastAPI with Django ORM.

You can add other Django Apps to it, and/or use Django Admin by mounting it at `/admin`.

## Features

- Devcontainer configuration;
- Dependabot configuration;
- Dockerfile for building the app;
- Docker Compose for running the app with PostgreSQL database in dev;
- FastAPI with some middleware and error handlers;

## How to use

1. Click on "Use this template" button;
2. Clone the repository;
3. Open the repository in VSCode;
4. Reopen the repository in a Devcontainer;
5. Edit as you wish (rename apps, devcontainer, services, etc.).


## Configuration

You can change settings in `mysite/settings` folder, and (most likely) need to change settings in `mysite/config.py` file.
The latter contains Pydantic Settings classes that are used to load settings from environment variables.
