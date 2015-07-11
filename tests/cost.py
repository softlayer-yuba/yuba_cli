# -*- coding: utf-8 -*-
import os

from SoftLayer import testing
from SoftLayer.testing import MockableTransport
from click import testing as click_testing
import logging

import yuba

LOGGER = logging.getLogger(__name__)

class FixtureTransport(object):
    """Implements a transport which returns fixtures."""

    fixture = {
        'generateOrderTemplate': {'hoge': 'fuga'}
    }

    def __call__(self, call):
        LOGGER.debug(call.method)
        return self.fixture[call.method]


class CostTest(testing.TestCase):
    @classmethod
    def setUpClass(cls):
        """Stand up fixtured/mockable XML-RPC server."""
        super(CostTest, cls).setUpClass()
        cls.mocks = MockableTransport(FixtureTransport())

    def run_command(self,
                    args=None,
                    env=None,
                    fixtures=True,
                    fmt='json'):
        """A helper that runs a SoftLayer-Yuba CLI command.

        This returns a click.testing.Result object.
        """
        args = args or []

        runner = click_testing.CliRunner()
        return runner.invoke(yuba.cli, args=args, obj=env or self.env)

    def test_cost(self):
        ret = self.run_command(['cost'])
        self.assertEqual(ret.exit_code, 2)

        test_file = os.path.join(os.path.dirname(__file__), 'test.yml')
        ret = self.run_command(['cost', test_file])
        self.assertEqual(ret.exit_code, 0)
