import click
import yaml

@click.command()
@click.argument('setting', type=click.File('r'), required=True)
def cli(setting):
    params = yaml.load(setting)
    print params
