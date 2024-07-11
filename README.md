<p align="center">
    <a href="https://www.hive.fi/" target="_blank">
        <img src="https://github.com/hivehelsinki/.github/blob/main/assets/logo.png?raw=true" width="128" alt="Hive logo" />
    </a>
</p>

<p align="center">
  <sub>Created by <a href="https://github.com/amedeomajer">Amedeo Majer (ame)</a> and <a href="https://github.com/jgengo">Jordane Gengo (titus)</a></sub>
</p>

<br><br>

## About home-cleaner

`home-cleaner` is a tool used at Hive Helsinki to detect inactive students via the 42 intra API and delete their student home image.

## Development (Docker only)
Prerequisites:
* Docker Compose V2 (aka `docker compose` without the `-` in between)
* Make

### Essentials
Get everything up and running:
```
make start
```
This starts the Docker containers for our app and a [WireMock](https://wiremock.org/) container which acts as a mock for homemaker-api
The _app_ and _tests_ directories are volume mapped to the `homecleaner` container.
You can also access the external services via port 8080.

Bring everything down:
```
make stop
```

For convenience, there's also `make restart` which runs `stop` and `start`.

### Testing
You can run the pytest test suite with:
```
make test
```

It doesn't matter whether you have the containers already running (i.e. if you have `make start` running in another shell window) or not, `make test` works either way.

### Linting
We are using `ruff` for linting, `ruff format` for automatic code formatting, and `mypy` for static type checking.
You can run all of them with:
```
make lint
```

### Python dependencies
To add or remove dependencies, modify _pyproject.toml_ and generate a fresh lock file with:
```
make update-dependencies
```
After doing changes related to the dependencies, remember to restart (it rebuilds as well) containers with `make restart` (or `make stop` + `make start`).


## Development (local Python environment)
Follow these instructions.

Prerequisites:
* Docker Compose V2 (aka `docker compose` without the `-` in between)
* Make
* Python 3.12
* Poetry 1.8.3

### Essentials

#### Creating the local Python environment
Create a poetry environment and install the dependencies:
```
poetry install
```

Activate the virtual environment (after this you won't need to type `poetry run ...`):
```
poetry shell
```

#### Running the service

You can start the Docker dependencies (WireMock container for homemaker-api) with:
```
make start-dependencies
```

### Testing
```
pytest
```

### Python dependencies
To add or remove dependencies, modify _pyproject.toml_ and get the latest versions of the dependencies and a fresh _poetry.lock_ with:
```
poetry update
```

### Linting with pre-commit
We are using `ruff` for linting, and `ruff format` for automatic code formatting.
For convenience, we have bundled them into a pre-commit configuration.
If you want to have pre-commit to automatically run on each commit:
```
pre-commit install
```

Or if you just want to run it over the whole codebase at times:
```
pre-commit run --all-files
```

### Running the app
```
python -m app.main
```

## URLs
The urls that are accessible from localhost:
* Homemaker-API (mocked): http://localhost:8080/api/v1/ (e.g. http://localhost:8080/api/v1/homes)

These work both in "Docker only" and "local Python environment" development setups.