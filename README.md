# generative-dating-agents

## Project Pitch

[**Project Pitch Document**](https://docs.google.com/document/d/1Kpphmy4kd4oYcwwQcB1siQmqY4DT5f1P6Vu5Du9Mxj4/edit#heading=h.qfapgtxugnfr)

## Setup

This project uses
python poetry for dependency management.
Follow instructions [here](https://python-poetry.org/docs/#installing-with-the-official-installer)
for installation. Clone this repository and run the following
command to install project dependencies in the project's
virtual environment.

```sh
poetry install
```

Once you've done that, activate the
project's python virtual environment.

```sh
poetry shell
```

## Running Locally CLI

The current working directory should be repository root.
Explore CLI commands.

```shell
 python3 -m src.generative_dating_agents.cli
```

### Generate User Profiles

These are already generated but if you'd
like to generate more you can run these commands.

* Set your OpenAI API key environment variable

```sh
export OPENAI_API_KEY={{YOUR OPEN AI KEY}}
```

This command will generate synthetic dating
user profiles images invoking OpenAI chat-completion
and text-to-image models. It runs serially. See default
arguments.

```sh
python3 -m src.generative_dating_agents.cli \
generate-user-profiles \
--n-profiles 10 \
--model "gpt-4-0613" \
--max-tokens 5000 \
--temperature 1.05
```

### Spin-up Vector DB

This command will loop over all synthetically generated users
and load them into a simple open source
persistent local vector database.
See [Chroma](https://docs.trychroma.com/usage-guide).

```sh
python3 -m src.generative_dating_agents.cli \
load-user-profile-collection \
--distance cosine
```

This command will query the vector database.

```shell
python3 -m src.generative_dating_agents.cli \
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
python3 -m src.generative_dating_agents.cli \
delete-user-profile-collection
```

## Matchmaking

Run matchmaking retrieval / ranking algorithm for a given user id.
Your OpenAI token must be set and the vector database must be loaded.
This command will attempt to find matches for the provided user id.

```shell
python3 -m src.generative_dating_agents.cli \
find-matches \
--user-id "f0e35556-8760-41ae-b0f9-4c777c48b170" \
--n-retrievals 20 \
--n-matches 5 \
--model "gpt-3.5-turbo-16k-0613" \
--max-tokens 5000 \
--temperature 0.0 \
--verbose False
```

This command will attempt to find matches for all user ids.
It takes a while as it loops over the function above
for all users sleeping in between users to prevent
rate limiting failure modes.

```shell
python3 -m src.generative_dating_agents.cli \
find-matches-for-all \
--n-retrievals 20 \
--n-matches 5 \
--model "gpt-3.5-turbo-16k-0613" \
--max-tokens 5000 \
--temperature 0.0 \
--verbose False
```

---

This project was generated using the [wolt-python-package-cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter) template.
