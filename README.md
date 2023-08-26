# generative-dating-agents

[![PyPI](https://img.shields.io/pypi/v/generative-dating-agents?style=flat-square)](https://pypi.python.org/pypi/generative-dating-agents/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/generative-dating-agents?style=flat-square)](https://pypi.python.org/pypi/generative-dating-agents/)
[![PyPI - License](https://img.shields.io/pypi/l/generative-dating-agents?style=flat-square)](https://pypi.python.org/pypi/generative-dating-agents/)
[![Coookiecutter - Wolt](https://img.shields.io/badge/cookiecutter-Wolt-00c2e8?style=flat-square&logo=cookiecutter&logoColor=D4AA00&link=https://github.com/woltapp/wolt-python-package-cookiecutter)](https://github.com/woltapp/wolt-python-package-cookiecutter)


---

**Documentation**: [https://deychak.github.io/generative-dating-agents](https://deychak.github.io/generative-dating-agents)

**Source Code**: [https://github.com/deychak/generative-dating-agents](https://github.com/deychak/generative-dating-agents)

**PyPI**: [https://pypi.org/project/generative-dating-agents/](https://pypi.org/project/generative-dating-agents/)

---

Generative Dating Agents

## Running

```shell
poetry install
```

### Generate User Profiles

```sh
export OPENAI_API_KEY={{YOUR OPEN AI KEY}}
```

```sh
python3 -m src.generative_dating_agents.cli generate-profiles
```

### Initialize Chroma Vector DB

Ensure the docker daemon is running.
Clone chroma repository as a sibling to this repository.

```shell
git clone https://github.com/chroma-core/chroma.git &&
cd chroma &&
docker-compose up -d --build
```

```shell
python3 -m src.generative_dating_agents.cli load-collection
```

```shell
python3 -m src.generative_dating_agents.cli query-collection --query-text "A multilingual straight male athlete"
```

```shell
python3 -m src.generative_dating_agents.cli delete-collection
```

## Installation

```sh
pip install generative-dating-agents
```

## Development

* Clone this repository
* Requirements:
  * [Poetry](https://python-poetry.org/)
  * Python 3.7+
* Create a virtual environment and install the dependencies

```sh
poetry install
```

* Activate the virtual environment

```sh
poetry shell
```

### Testing

```sh
pytest
```

### Documentation

The documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings
 of the public signatures of the source code. The documentation is updated and published as a [Github project page
 ](https://pages.github.com/) automatically as part each release.

### Releasing

Trigger the [Draft release workflow](https://github.com/deychak/generative-dating-agents/actions/workflows/draft_release.yml)
(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.

Find the draft release from the
[GitHub releases](https://github.com/deychak/generative-dating-agents/releases) and publish it. When
 a release is published, it'll trigger [release](https://github.com/deychak/generative-dating-agents/blob/master/.github/workflows/release.yml) workflow which creates PyPI
 release and deploys updated documentation.

### Pre-commit

Pre-commit hooks run all the auto-formatters (e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), and other quality
 checks to make sure the changeset is in good shape before a commit/push happens.

You can install the hooks with (runs for each commit):

```sh
pre-commit install
```

Or if you want them to run only for each push:

```sh
pre-commit install -t pre-push
```

Or if you want e.g. want to run all checks manually for all files:

```sh
pre-commit run --all-files
```

---

This project was generated using the [wolt-python-package-cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter) template.
