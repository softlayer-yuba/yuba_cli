import operator
from os.path import expanduser
import click
import SoftLayer
import yaml
from jinja2 import Template

from pprint import pprint

@click.group()
@click.pass_context
def cli(ctx):
    pass

@cli.command()
@click.argument('setting', type=click.File('r'), required=True)
@click.option('--config', type=click.File('r'), default=expanduser('~/.yuba/config.yml'))
@click.option('--order/--no-order', default=False, help='Order instances')
def cost(setting, config, order):
    config = yaml.load(config)
    params = yaml.load(Template(setting.read()).render(config))
    pprint(params)

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
    pprint(total)

    if order:
        print 'Ordering instances...'
        result = vsi.create_instances(instance_settings)
        pprint(result)

        not_available = []
        for tmp in result:
            machine_id = tmp['id']
            if not vsi.wait_for_ready(machine_id, 600, pending=True):
                print 'machine_id: %s is not available' % machine_id
                not_available.append(machine_id)
            else:
                print 'machine_id: %s is available' % machine_id

def calculate_total(result):
    total_monthly = 0.0
    total_hourly = 0.0

    for price in result['prices']:
        total_monthly += float(price.get('recurringFee', 0.0))
        total_hourly += float(price.get('hourlyRecurringFee', 0.0))

    return total_monthly, total_hourly
