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
from .matching.match import find_matches as _find_matches


@click.command()
@click.option(
    "--n-profiles", type=int, default=10, help="Number of user profiles to generate."
)
@click.option("--model", type=str, default="gpt-4-0613", help="OpenAI model name.")
@click.option("--max-tokens", type=int, default=5000, help="OpenAI model max tokens.")
@click.option(
    "--temperature", type=float, default=1.05, help="OpenAI model temperature."
)
def generate_user_profiles(
    n_profiles: int,
    model: str,
    max_tokens: int,
    temperature: float,
) -> None:
    click.echo("Generating user profiles")
    _generate_profiles(
        n_profiles=n_profiles,
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
@click.option(
    "--user-id",
    type=str,
    default="f0e35556-8760-41ae-b0f9-4c777c48b170",
    help="Query matching user id.",
)
@click.option(
    "--n-retrievals", type=int, default=20, help="Number of retrieved user profiles."
)
@click.option(
    "--n-matches", type=int, default=5, help="Number of ranked user profiles."
)
@click.option(
    "--model", type=str, default="gpt-3.5-turbo-16k-0613", help="OpenAI model name."
)
@click.option("--max-tokens", type=int, default=5000, help="OpenAI model max tokens.")
@click.option(
    "--temperature", type=float, default=0.0, help="OpenAI model temperature."
)
def find_matches(
    user_id: str,
    n_retrievals: int,
    n_matches: int,
    model: str,
    temperature: float,
    max_tokens: int,
) -> None:
    click.echo("Finding candidate user matches")
    _find_matches(
        user_id=user_id,
        n_retrievals=n_retrievals,
        n_matches=n_matches,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        verbose=True,
    )
    click.echo("Successfully found candidate user matches")


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
cli.add_command(find_matches)

if __name__ == "__main__":
    cli()
