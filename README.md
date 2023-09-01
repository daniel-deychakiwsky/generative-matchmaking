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

## Project Pitch

[**Project Pitch Document**](https://docs.google.com/document/d/1Kpphmy4kd4oYcwwQcB1siQmqY4DT5f1P6Vu5Du9Mxj4/edit#heading=h.qfapgtxugnfr)

## Bootstrapping / Development

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

## Running Locally CLI

Current working directory should be repository root.
Explore CLI commands.

```shell
 python3 -m src.generative_dating_agents.cli
```

### Generate User Profiles

OpenAI balance must be funded.
Set your OpenAI API key env var.

```sh
export OPENAI_API_KEY={{YOUR OPEN AI KEY}}
```

Generate dating user profiles and profile images with defaults.
Invokes OpenAI LLM and text-to-image. Haven't had issues with
rate limiting running this.

```sh
python3 -m src.generative_dating_agents.cli generate-user-profiles
```

### Loading and Querying Vector DB

[Chroma](https://docs.trychroma.com/usage-guide)
is a simple open source vector database
that will use a local persistent directory.

```shell
python3 -m src.generative_dating_agents.cli load-user-profile-collection
```

Query collection with defaults.

```shell
python3 -m src.generative_dating_agents.cli query-user-profile-collection --n-results 5 --query-text \
"The user is seeking a man between the ages of 30 and 40,
who is at least 5'8\" and no taller than 6'3\". He should
have no children but wish to have them in the future. His
sexual orientation should be straight and he should be
someone who drinks sometimes, but does not smoke, use
marijuana, or other drugs. He should live an active
lifestyle. His ethnicity could be White Caucasian, East
Asian, or Hispanic/Latino and he should have liberal or
moderate political beliefs. Ideal occupations would be
within the Technology, Science, or Education industries.
He must speak English and have similar values, specifically
Honesty, Family, Responsibility, Respect, and Fairness.
His interests could include Technology, Outdoors, Cinema,
Reading, and Sports. The prospective partner should have
at least an undergraduate level education, with intentions
for long-term dating and a preference for monogamy."
```

Delete collection with defaults.

```shell
python3 -m src.generative_dating_agents.cli delete-user-profile-collection
```

## Matchmaking

OpenAI balance must be funded.

Run matchmaking retrieval / ranking algorithm for given user id.
Requires steps from above: OpenAI token set, generated users, and loaded vector database.

Find matches for one user id with defaults.

```shell
python3 -m src.generative_dating_agents.cli find-matches --user-id "f0e35556-8760-41ae-b0f9-4c777c48b170"
```

Find matches for all user ids with defaults.
This takes a while as it loops over the function above
for all users sleeping in between users to prevent rate limiting failure modes.

```shell
python3 -m src.generative_dating_agents.cli find-matches-for-all
```

## Installation as Package

```sh
pip install generative-dating-agents
```

### Testing

```sh
pytest
```

### Documentation

The documentation is automatically generated from the
content of the [docs directory](./docs) and from the docstrings
of the public signatures of the source code.
The documentation is updated and published as a [Github project page
 ](https://pages.github.com/) automatically as part each release.

### Releasing

Trigger the [Draft release workflow](https://github.com/deychak/generative-dating-agents/actions/workflows/draft_release.yml)
(press _Run workflow_).
This will update the changelog & version and create a GitHub
release which is in _Draft_ state.

Find the draft release from the
[GitHub releases](https://github.com/deychak/generative-dating-agents/releases)
and publish it. When a release is published, it'll trigger
[release](https://github.com/deychak/generative-dating-agents/blob/master/.github/workflows/release.yml)
workflow which creates PyPI release and deploys updated documentation.

### Pre-commit

Pre-commit hooks run all the auto-formatters (e.g. `black`, `isort`),
linters (e.g. `mypy`, `flake8`), and other quality
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
