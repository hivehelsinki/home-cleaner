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


## Development (local Python environment)
Follow these instructions.

Prerequisites:
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

TODO

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