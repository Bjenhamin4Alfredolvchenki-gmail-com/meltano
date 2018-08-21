import click
import os
from extract.fastly.extractor import FastlyExtractor
from extract.demo.extractor import DemoExtractor
from load.postgres.loader import PostgresLoader
from load.csv.loader import CsvLoader


@click.group()
def cli():
    pass


# TODO: to be generated from the file structure of /Extract/
EXTRACTOR_REGISTRY = {
    'fastly': FastlyExtractor,
    'demo': DemoExtractor
}

LOADER_REGISTRY = {
    'postgres': PostgresLoader,
    'csv': CsvLoader,
}


def run_extract(
        extractor_name,
        loader_name,
        host=os.environ.get('PG_ADDRESS'),
        port=os.environ.get('PG_PORT'),
        database=os.environ.get('PG_DATABASE'),
        username=os.environ.get('PG_USERNAME'),
        password=os.environ.get('PG_PASSWORD'),
):
    """
    :param host: db hostname
    :param port:
    :param database: name of the database to load to
    :param username: rolename with wright access to the db
    :param password:
    :param extractor_name:
    :param loader_name:
    :return:
    """
    click.echo(f"Loading and initializing extractor: {extractor_name}")
    extractor_class = EXTRACTOR_REGISTRY.get(extractor_name)
    if not extractor_class:
        raise Exception(
            f'Extractor {extractor_name} not found please specify one of the following: {EXTRACTOR_REGISTRY.keys()}'
        )
    extractor = extractor_class()
    click.echo(f"Loading and initializing loader: {loader_name}")
    loader_class = LOADER_REGISTRY.get(loader_name)
    if not loader_class:
        raise Exception(
            f'Loader {loader_name} not found please specify one of the following: {LOADER_REGISTRY.keys()}'
        )
    connection_string = f'postgresql://{username}:{password}@{host}:{port}/{database}'
    click.echo("Starting extraction ... ")

    loader = loader_class(
        connection_string=connection_string,
        extractor=extractor,
    )
    click.echo("Applying the schema ... ")
    loader.schema_apply()
    entities_gen = extractor.extract()
    results = set()
    for entity in entities_gen:
        for entity_name, df in entity.items():
            click.echo("Got extractor results, loading them into the loader")
            results.add(loader.load(df=df, schema_name=entity_name))
            click.echo("Load done! Exiting")
    return results


@cli.command()
@click.argument('extractor_name')
@click.option('--loader_name', default='postgres', help="Which loader should be used in this extraction")
# @click.option('-S', '--schema', required=True)
@click.option('-H', '--host',
              envvar='PG_ADDRESS',
              default='localhost',
              help="Database schema to use.")
@click.option('-p', '--port',
              type=int,
              envvar='PG_PORT',
              default=5432)
@click.option('-d', '-db', 'database',
              envvar='PG_DATABASE',
              help="Database to import the data to.")
@click.option('-u', '--username', envvar='PG_USERNAME',
              help="Specifies the user to connect to the database with.")
@click.password_option(envvar='PG_PASSWORD')
def extract(extractor_name, loader_name, host, port, database, username, password):
    run_extract(extractor_name, loader_name, host, port, database, username, password)


if __name__ == '__main__':
    cli()