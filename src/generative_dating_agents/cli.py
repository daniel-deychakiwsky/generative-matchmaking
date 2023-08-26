import click

from .data.users import generate_profiles as _generate_profiles
from .database.chroma import delete_collection as _delete_collection
from .database.chroma import load_collection as _load_collection
from .database.chroma import query_collection as _query_collection


@click.command()
@click.option(
    "--num-profiles", type=int, default=10, help="Number of user profiles to generate."
)
@click.option("--model", type=str, default="gpt-4-0613", help="OpenAI model name.")
@click.option("--max-tokens", type=int, default=5000, help="OpenAI model max tokens.")
@click.option(
    "--temperature", type=float, default=1.05, help="OpenAI model temperature."
)
@click.option(
    "--output-directory",
    type=str,
    default="profiles",
    help="Output user profile directory",
)
@click.option(
    "--output-file-name",
    type=str,
    default="profile.json",
    help="Output user profile file name",
)
@click.option(
    "--output-image-file-name",
    type=str,
    default="profile.png",
    help="Output user profile file name",
)
@click.option("--n-jobs", type=int, default=2, help="OpenAI generation parallelism.")
def generate_profiles(
    num_profiles: int,
    model: str,
    max_tokens: int,
    temperature: float,
    output_directory: str,
    output_file_name: str,
    output_image_file_name: str,
    n_jobs: int,
) -> None:
    click.echo("Generating user profiles")
    _generate_profiles(
        num_profiles=num_profiles,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        output_directory=output_directory,
        output_file_name=output_file_name,
        output_image_file_name=output_image_file_name,
        n_jobs=n_jobs,
    )
    click.echo("Successfully generated user profiles")


@click.command()
@click.option(
    "--input-directory",
    type=str,
    default="profiles",
    help="Input user profiles directory",
)
@click.option(
    "--input-file-name",
    type=str,
    default="profile.json",
    help="Input user profiles file name",
)
@click.option(
    "--collection-name",
    type=str,
    default="user_profiles",
    help="Chroma collection name.",
)
@click.option(
    "--distance",
    type=click.Choice(choices=["cosine", "l2", "ip"], case_sensitive=True),
    default="cosine",
    help="Chroma collection distance function.",
)
def load_collection(
    input_directory: str, input_file_name: str, collection_name: str, distance: str
) -> None:
    click.echo("Loading database collection")
    _load_collection(
        input_directory=input_directory,
        input_file_name=input_file_name,
        collection_name=collection_name,
        distance=distance,
    )
    click.echo("Successfully loaded database collection")


@click.command()
@click.option(
    "--collection-name",
    type=str,
    default="user_profiles",
    help="Chroma collection name.",
)
@click.option("--query-text", type=str, help="Chroma query text.")
@click.option(
    "--n-results", type=int, default=2, help="Chroma number of query results."
)
def query_collection(collection_name: str, query_text: str, n_results: int) -> None:
    click.echo("Querying database collection")
    result = _query_collection(
        collection_name=collection_name,
        query_texts=[query_text],
        n_results=n_results,
        where=None,
        where_document=None,
    )
    click.echo("Successfully queried database collection")
    click.echo(result)


@click.command()
@click.option(
    "--collection-name",
    type=str,
    default="user_profiles",
    help="Chroma collection name.",
)
def delete_collection(collection_name: str) -> None:
    click.echo("Deleting database collection")
    _delete_collection(
        collection_name=collection_name,
    )
    click.echo("Successfully deleted database collection")


@click.group()
def cli() -> None:
    pass


cli.add_command(generate_profiles)
cli.add_command(load_collection)
cli.add_command(query_collection)
cli.add_command(delete_collection)

if __name__ == "__main__":
    cli()
