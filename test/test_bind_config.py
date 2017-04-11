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

    def test_key_number(self):
        testdata = {'key': 3}
        result = 'key 3;\n'
        self.renderTest(testdata, result)

    def test_ordred_keys(self):
        testdata = {'keyd': 'valued', 'keya': 'valuea', 'keyc': 'valuec', 'keyb': 'valueb'}
        result = 'keya valuea;\nkeyb valueb;\nkeyc valuec;\nkeyd valued;\n'
        self.renderTest(testdata, result)

    def test_unordered_keys(self):
        testdata = [{'keyd': 'valued'}, {'keyc': 'valuec'}, {'keyb': 'valueb'}, {'keya': 'valuea'}]
        result = 'keyd valued;\nkeyc valuec;\nkeyb valueb;\nkeya valuea;\n'
        self.renderTest(testdata, result)

    def test_nested_keys(self):
        testdata = {'outerKey': {'innerKey': 'innerValue'}}
        result = 'outerKey {\n  innerKey innerValue;\n};\n'
        self.renderTest(testdata, result)

    def test_multi_nested_keys(self):
        testdata = {'outerKey': {'middleKey': {'innerKey': 'innerValue'}}}
        result = 'outerKey {\n  middleKey {\n    innerKey innerValue;\n  };\n};\n'
        self.renderTest(testdata, result)

    def test_key_nested_list(self):
        testdata = {'key': ['item1', 'item2', 'item3']}
        result = 'key {\n  item1;\n  item2;\n  item3;\n};\n'
        self.renderTest(testdata, result)

    def test_multi_list(self):
        testdata = {'deny-answer-addresses': {'list': ['item1', 'item2'], 'followup': {'except-from': ['exp1', 'exp2']}}}
        result = 'deny-answer-addresses {\n  item1;\n  item2;\n} except-from {\n  exp1;\n  exp2;\n};\n'
        self.renderTest(testdata, result)

    def test_multi_list_deny_answerr_aliases(self):
        testdata = {'deny-answer-aliases': {'list': ['item1', 'item2'], 'followup': {'except-from': ['exp1', 'exp2']}}}
        result = 'deny-answer-aliases {\n  item1;\n  item2;\n} except-from {\n  exp1;\n  exp2;\n};\n'
        self.renderTest(testdata, result)

    def test_multi_list_without_followup(self):
        testdata = {'deny-answer-aliases': {'list': ['item1', 'item2']}}
        result = 'deny-answer-aliases {\n  item1;\n  item2;\n};\n'
        self.renderTest(testdata, result)

    def test_multi_list_without_first_list(self):
        testdata = {'deny-answer-aliases': {'followup': {'except-from': ['exp1', 'exp2']}}}
        result = 'deny-answer-aliases  except-from {\n  exp1;\n  exp2;\n};\n'
        self.renderTest(testdata, result)

if __name__ == '__main__':
    unittest.main()
