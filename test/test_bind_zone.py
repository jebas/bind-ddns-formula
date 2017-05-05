#!/usr/bin/python

import os, unittest
from jinja2 import Environment, FileSystemLoader

class TestZoneFile(unittest.TestCase):

    def setUp(self):
        self.t_dir = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            'bind-ddns',
            'templates'))
        self.t_conf = Environment(loader=FileSystemLoader(self.t_dir),
            trim_blocks=True)

    def renderTest(self, data, result):
        holder = self.t_conf.get_template('zone.jinja').render(testdata=data)
        output = repr(holder) + ' did not equal ' + repr(result)
        self.assertEqual(holder, result, output)

    def test_comment_line(self):
        testdata = {'zone': 'zone1'}
        holder = self.t_conf.get_template('zone.jinja').render(testdata=testdata)
        lines = holder.split("\n")
        self.assertEqual(lines[0], "; zone file for zone1",
                '"' + lines[0] + '" did not equal "; zone file for zone1"')

if __name__ == '__main__':
    unittest.main()
