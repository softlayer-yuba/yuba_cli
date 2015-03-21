import operator
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
    instance_settings = []
    total = (0.0, 0.0)
    for hostname, param in params.items():
        param.setdefault('hostname', hostname)

        result = vsi.verify_create_instance(**param)
        pprint(result)

        tmp_total = calculate_total(result)
        total = map(operator.add, total, tmp_total)
        pprint(tmp_total)

        instance_settings.append(param)

    result = vsi.create_instances(instance_settings)
    pprint(total)
    pprint(result)

def calculate_total(result):
    total_monthly = 0.0
    total_hourly = 0.0

    for price in result['prices']:
        total_monthly += float(price.get('recurringFee', 0.0))
        total_hourly += float(price.get('hourlyRecurringFee', 0.0))

    return total_monthly, total_hourly

