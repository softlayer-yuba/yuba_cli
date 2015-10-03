# -*- coding: utf-8 -*-
import os

from SoftLayer import testing
from click import testing as click_testing

import yuba


class CostTest(testing.TestCase):

    def run_command(self, *args, **kwargs):
        runner = click_testing.CliRunner()
        return runner.invoke(yuba.cli, args=args)

    def test_cost(self):
        ret = self.run_command('cost')
        self.assertEqual(ret.exit_code, 2)
        return

        test_file = os.path.join(os.path.dirname(__file__), 'test.yml')
        ret = self.run_command('cost', test_file)
        self.assertEqual(ret.exit_code, 0)
