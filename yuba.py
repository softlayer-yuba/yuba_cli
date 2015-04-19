import operator
from os.path import expanduser
import click
import SoftLayer
from SoftLayer.CLI import formatting
import yaml
from jinja2 import Template

from pprint import pprint

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.obj = {}
    ctx.obj['DEBUG'] = debug

@cli.command()
@click.argument('setting', type=click.File('r'), required=True)
@click.option('--config', type=click.File('r'), default=expanduser('~/.yuba/config.yml'))
@click.pass_context
def cost(ctx, setting, config):
    config = yaml.load(config)
    params = yaml.load(Template(setting.read()).render(config))
    if ctx.obj['DEBUG']:
        pprint(params)

    client = SoftLayer.Client()

    vsi = SoftLayer.VSManager(client)
    instance_settings = []
    total = (0.0, 0.0)
    total_result = formatting.Table(['monthly', 'hourly'])
    for hostname, param in params.items():
        price_table = formatting.Table(['name', 'monthly', 'hourly'])
        price_table.align['name'] = 'l'
        price_table.align['monthly'] = 'r'
        price_table.align['hourly'] = 'r'
        param.setdefault('hostname', hostname)

        result = vsi.verify_create_instance(**param)
        
        for v in result['prices']:
            price_table.add_row([
                v['item']['description'],
                v.get('recurringFee', '-'),
                v.get('hourlyRecurringFee'),
            ])
        print formatting.format_output(price_table)

        tmp_total = calculate_total(result)
        total = map(operator.add, total, tmp_total)

        instance_settings.append(param)
    total_result.add_row(total)
    print formatting.format_output(total_result)



def calculate_total(result):
    total_monthly = 0.0
    total_hourly = 0.0

    for price in result['prices']:
        total_monthly += float(price.get('recurringFee', 0.0))
        total_hourly += float(price.get('hourlyRecurringFee', 0.0))

    return total_monthly, total_hourly

@cli.command()
@click.argument('setting', type=click.File('r'), required=True)
@click.option('--config', type=click.File('r'), default=expanduser('~/.yuba/config.yml'))
@click.option('--order/--no-order', default=False, help='Order instances')
def order(setting, config, order):
    config = yaml.load(config)
    params = yaml.load(Template(setting.read()).render(config))
    pprint(params)

    client = SoftLayer.Client()

    vsi = SoftLayer.VSManager(client)
    instance_settings = [v for v in params.values()]

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

