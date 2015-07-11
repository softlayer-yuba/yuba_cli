# -*- coding: utf-8 -*-
import os
import mock

import SoftLayer
from SoftLayer import testing
from click import testing as click_testing

import yuba


def fake(*args, **kwargs):
    client = SoftLayer.BaseClient(
        transport=SoftLayer.FixtureTransport(),
        auth=None,
    )
    return client


dummy_verify_order_return = {
    'complexType': 'SoftLayer_Container_Product_Order_Virtual_Guest',
    'location': '449604',
    'prices': [
        {
            'item': {'description': '1 x 2.0 GHz Core'},
            'hourlyRecurringFee': '.023',
            'recurringFee': '15',
            'id': 1640
        },
        {
            'item': {'description': '1 GB'},
            'hourlyRecurringFee': '.015',
            'recurringFee': '10',
            'id': 1644
        },
        {
            'item': {'description': 'CentOS 7.x - Minimal Install (64 bit)'},
            'hourlyRecurringFee': '0',
            'recurringFee': '0',
            'id': 45466
        },
        {
            'item': {'description': '25 GB (LOCAL)'},
            'hourlyRecurringFee': '0',
            'recurringFee': '0',
            'id': 13899
            },
        {
            'item': {'description': 'Host Ping'},
            'hourlyRecurringFee': '0',
            'recurringFee': '0',
            'id': 55
        },
        {
            'item': {'description': 'Email and Ticket'},
            'hourlyRecurringFee': '0',
            'recurringFee': '0',
            'id': 57
        },
        {
            'item': {'description': 'Automated Notification'},
            'hourlyRecurringFee': '0',
            'recurringFee': '0',
            'id': 58
        },
        {
            'item': {'description': '10 Mbps Public & Private Network Uplinks'},
            'hourlyRecurringFee': '0',
            'recurringFee': '0',
            'id': 272
        },
        {
            'item': {'description': '0 GB Bandwidth'},
            'hourlyRecurringFee': '0',
            'id': 1800
        },
        {
            'item': {'description': 'Unlimited SSL VPN Users & 1 PPTP VPN User per account'},
            'hourlyRecurringFee': '0',
            'recurringFee': '0',
            'id': 420
        },
        {
            'item': {'description': 'Nessus Vulnerability Assessment & Reporting'},
            'hourlyRecurringFee': '0',
            'recurringFee': '0',
            'id': 418
        },
        {
            'item': {'description': 'Reboot / Remote Console'},
            'hourlyRecurringFee': '0',
            'recurringFee': '0',
            'id': 905
        },
        {
            'item': {'description': '1 IP Address'},
            'hourlyRecurringFee': '0',
            'recurringFee': '0',
            'id': 21
        }],
    'imageTemplateId': '',
    'packageId': 46,
    'sourceVirtualGuestId': '',
    'useHourlyPricing': True,
    'virtualGuests': [{'domain': 'maisuto.jp', 'hostname': 'vs000'}],
    'sshKeys': [],
    'quantity': 1
}


class CostTest(testing.TestCase):

    def run_command(self, *args, **kwargs):
        runner = click_testing.CliRunner()
        return runner.invoke(yuba.cli, args=args)

    @mock.patch.dict(
        'SoftLayer.testing.fixtures.SoftLayer_Virtual_Guest.generateOrderTemplate',
        dummy_verify_order_return
    )
    @mock.patch('SoftLayer.Client', fake)
    def test_cost(self):
        ret = self.run_command('cost')
        self.assertEqual(ret.exit_code, 2)

        test_file = os.path.join(os.path.dirname(__file__), 'test.yml')
        ret = self.run_command('cost', test_file)
        self.assertEqual(ret.exit_code, 0)
