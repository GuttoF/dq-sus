import click
from dq_sus.extract.get_raw import extract_parquet
from dq_sus.transform.transform_db import transform_db

@click.group()
def cli() -> None:
    """Command Line Interface for dq_sus"""
    pass

@cli.command()
@click.option("--disease", prompt="Disease", help="Disease to extract data for")
@click.option("--years", prompt="Years", help="Years to extract", type=str)

def extract(disease: str, years: str) -> None:
    years_list = [int(year) for year in years.split(',')]
    files = extract_parquet(disease, years_list)
    click.echo(f"Extracted files: {files}")

@cli.command()
def transform() -> None:
    transform_db()
    click.echo("Database transformed successfully!")

if __name__ == "__main__":
    cli()
