from typing import List

import click

from .data.users import generate_profiles as _generate_profiles
from .database.chroma import (
    delete_user_profile_collection as _delete_user_profile_collection,
)
from .database.chroma import (
    load_user_profile_collection as _load_user_profile_collection,
)
from .database.chroma import (
    query_user_profile_collection as _query_user_profile_collection,
)


@click.command()
@click.option(
    "--num-profiles", type=int, default=10, help="Number of user profiles to generate."
)
@click.option("--model", type=str, default="gpt-4-0613", help="OpenAI model name.")
@click.option("--max-tokens", type=int, default=5000, help="OpenAI model max tokens.")
@click.option(
    "--temperature", type=float, default=1.05, help="OpenAI model temperature."
)
def generate_user_profiles(
    num_profiles: int,
    model: str,
    max_tokens: int,
    temperature: float,
) -> None:
    click.echo("Generating user profiles")
    _generate_profiles(
        num_profiles=num_profiles,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    click.echo("Successfully generated user profiles")


@click.command()
@click.option(
    "--distance",
    type=click.Choice(choices=["cosine", "l2", "ip"], case_sensitive=True),
    default="cosine",
    help="Chroma collection distance function.",
)
def load_user_profile_collection(distance: str) -> None:
    click.echo("Loading database collection")
    _load_user_profile_collection(
        distance=distance,
        verbose=True,
    )
    click.echo("Successfully loaded database collection")


@click.command()
@click.option("--query-text", type=str, multiple=True, help="Chroma query texts.")
@click.option(
    "--n-results", type=int, default=2, help="Chroma number of query results."
)
def query_user_profile_collection(query_text: List[str], n_results: int) -> None:
    click.echo("Querying database collection")
    _query_user_profile_collection(
        query_texts=query_text,
        n_results=n_results,
        where=None,
        where_document=None,
        verbose=True,
    )
    click.echo("Successfully queried database collection")


@click.command()
def delete_user_profile_collection() -> None:
    click.echo("Deleting database collection")
    _delete_user_profile_collection()
    click.echo("Successfully deleted database collection")


@click.group()
def cli() -> None:
    pass


cli.add_command(generate_user_profiles)
cli.add_command(load_user_profile_collection)
cli.add_command(query_user_profile_collection)
cli.add_command(delete_user_profile_collection)

if __name__ == "__main__":
    cli()
