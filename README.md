# Generative Matchmaking

## Overview

TODO

## Running

### Setup

This project uses poetry for python dependency management.
Follow the instructions [here](https://python-poetry.org/docs/#installing-with-the-official-installer)
for installation. Once, you've done that, clone this repository and run the following
command to install the project's dependencies within the poetry-created
virtual environment.

```sh
poetry install
```

Once you've done that, activate the
project's python virtual environment.

```sh
poetry shell
```

### Command Line Interface (CLI)

CLI commands assume repo root as current working directory.

The following command will list available CLI commands.

```shell
 python3 -m src.generative_matchmaking.cli
```

#### Generate User Profiles

This step can be skipped since these
are **already generated**.

If you'd like to generate more on your own,
run the following commands to set your OpenAI
API key environment variable and
generate synthetic dating user profiles.

```sh
export OPENAI_API_KEY="{{YOUR OPEN AI KEY}}"
```

```sh
python3 -m src.generative_matchmaking.cli \
generate-user-profiles \
--n-profiles 5 \
--model "gpt-4-0613" \
--max-tokens 5000 \
--temperature 1.05
```

#### Vectorizing User Profiles

This command will loop over all synthetically generated users
and load them into a simple open source
locally persistent vector database.
See [Chroma](https://docs.trychroma.com/usage-guide).

```sh
python3 -m src.generative_matchmaking.cli \
load-user-profile-collection \
--distance cosine
```

This command will query the vector database.

```shell
python3 -m src.generative_matchmaking.cli \
query-user-profile-collection \
--n-results 5 \
--verbose True \
--query-text \
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

This command deletes the loaded collection.

```shell
python3 -m src.generative_matchmaking.cli \
delete-user-profile-collection
```

#### Matchmaking

These are **already generated** but if you'd
like to regenerate or generate more you can run these commands.

This command will run the matchmaking
algorithm for a given user id.

```shell
python3 -m src.generative_matchmaking.cli \
find-matches \
--user-id "f0e35556-8760-41ae-b0f9-4c777c48b170" \
--n-matches 5
```

This command will do the same but for all user ids sequentially.

```shell
python3 -m src.generative_matchmaking.cli \
find-matches-for-all \
--n-matches 25
```

---

This project was generated using the [wolt-python-package-cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter) template.
