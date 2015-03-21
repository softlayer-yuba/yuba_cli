import click
import SoftLayer
import yaml

from pprint import pprint

@click.command()
@click.argument('setting', type=click.File('r'), required=True)
def cli(setting):
    params = yaml.load(setting)
    print params

    client = SoftLayer.Client()

    vsi = SoftLayer.VSManager(client)
    result = vsi.verify_create_instance(**params)
    pprint(result)

    # result = vsi.create_instance(**params)
    # pprint(result)
