#!/usr/bin/python

import os, unittest
from jinja2 import Environment, FileSystemLoader

class TestBindConfig(unittest.TestCase):

    def setUp(self):
        self.t_dir = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            'bind-ddns',
            'templates'))
        self.t_conf = Environment(loader=FileSystemLoader(self.t_dir), 
            trim_blocks=True)

    def renderTest(self, data, result):
        holder = self.t_conf.get_template('test_config.jinja').render(testdata=data)
        output = repr(holder) + ' did not equal ' + repr(result)
        self.assertEqual(holder, result, output)

    def test_string(self):
        testdata = 'stuff'
        result = 'stuff;\n'
        self.renderTest(testdata, result)

    def test_number(self):
        testdata = 3
        result = '3;\n'
        self.renderTest(testdata, result)

    def test_key_value(self):
        testdata = {'key': 'value'}
        result = 'key value;\n'
        self.renderTest(testdata, result)

    def test_ordred_keys(self):
        testdata = {'keyd': 'valued', 'keya': 'valuea', 'keyc': 'valuec', 'keyb': 'valueb'}
        result = 'keya valuea;\nkeyb valueb;\nkeyc valuec;\nkeyd valued;\n'
        self.renderTest(testdata, result)

    def test_unordered_keys(self):
        testdata = [{'keyd': 'valued'}, {'keyc': 'valuec'}, {'keyb': 'valueb'}, {'keya': 'valuea'}]
        result = 'keyd valued;\nkeyc valuec;\nkeyb valueb;\nkeya valuea;\n'
        self.renderTest(testdata, result)

if __name__ == '__main__':
    unittest.main()
