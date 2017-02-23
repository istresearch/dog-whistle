from unittest import TestCase
from dog_whistle import *
from dog_whistle import _get_config, _reset
import sys
from mock import patch, MagicMock

# from http://stackoverflow.com/questions/4219717/how-to-assert-output-with-nosetest-unittest-in-python
from contextlib import contextmanager
from StringIO import StringIO
@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class DogWhistleTest(TestCase):

    def test_01_analyze_blank(self):
        expected = 'It does not appear like the LogFactory is used in this project'

        with captured_output() as (out, err):
            dw_analyze('./tests/example1')

        output = out.getvalue().strip()
        self.assertEqual(output, expected)

    def test_02_analyze_found_lf(self):
        expected = "You don't appear to have any logger statements.\n\nAuto-Generated Template Settings\n--------------------------------\n\ndw_dict = {\n    'name': '<my_project>',\n    'tags': [\n        # high level tags that everything in your app will have\n        'item:descriptor'\n    ],\n    'metrics': {\n        # By default, everything is a counter using the concatentated log string\n        # the 'counters' key is NOT required, it is shown here for illustration\n        'counters': [\n            # datadog metrics that will use ++\n        ],\n        # datadog metrics that have a predefined value like `51`\n        # These metrics override any 'counter' with the same key,\n        # and are shown here for illustration purposes only\n        'gauges': [\n            \n        ]\n    },\n    'options': {\n        # use statsd for local testing, see docs\n        'statsd_host': 'localhost',\n        'statsd_port': 8125,\n        'local': True,\n    },\n\n}\n\nEnsure the above dictionary is passed into `dw_config()`"

        with captured_output() as (out, err):
            dw_analyze('./tests/example2')

        output = out.getvalue().strip()
        self.assertEqual(output, expected)

    def test_03_analyze_found_logs(self):
        expected = 'Valid Lines\n-----------\n./tests/example3/example.py\n   3 : logger.info("hey this is a message")\n   5 : logger.warn("stuff", extras)\n\nInvalid Lines\n-------------\n\n<<<<<<<<<< YOU MUST FIX THESE BEFORE USING THE DOGWHISTLE LIBRARY >>>>>>>>>>>\n\n./tests/example3/example.py\n   7 : logger.info("bad" + str(val), extras)\n\nAuto-Generated Template Settings\n--------------------------------\n\ndw_dict = {\n    \'name\': \'<my_project>\',\n    \'tags\': [\n        # high level tags that everything in your app will have\n        \'item:descriptor\'\n    ],\n    \'metrics\': {\n        # By default, everything is a counter using the concatentated log string\n        # the \'counters\' key is NOT required, it is shown here for illustration\n        \'counters\': [\n            # datadog metrics that will use ++\n            ("hey this is a message", "hey_this_is_a_message"),\n            ("stuff", "stuff"),\n        ],\n        # datadog metrics that have a predefined value like `51`\n        # These metrics override any \'counter\' with the same key,\n        # and are shown here for illustration purposes only\n        \'gauges\': [\n            \n            ("stuff", "stuff", "<extras.key.path>"),\n        ]\n    },\n    \'options\': {\n        # use statsd for local testing, see docs\n        \'statsd_host\': \'localhost\',\n        \'statsd_port\': 8125,\n        \'local\': True,\n    },\n\n}\n\nEnsure the above dictionary is passed into `dw_config()`'

        with captured_output() as (out, err):
            dw_analyze('./tests/example3')

        output = out.getvalue().strip()
        self.assertEqual(output, expected)

    def test_04_config_no_name(self):
        bad = {'key': 'value'}

        with self.assertRaises(Exception) as e:
            dw_config(bad)
        self.assertEquals(e.exception.message, "'name' key required in dog_whistle config")

    def test_05_config_bad_statsd(self):
        configs = {
            'name': 'cool',
            'tags': [
                'list:strings'
            ],
            'metrics': {
                'counters': [('message', 'dd.key')],
                'gauges': [("Too high!", "too_high", "<extras.key.path>"),],
            },
            'options': {
                'statsd_port': 8125,
                'local': True,
            }
        }

        with self.assertRaises(Exception) as e:
            dw_config(configs)
        self.assertEquals(e.exception.message, "Unknown statsd config for local setup")

    def test_06_config_statsd(self):
        configs = {
            'name': 'cool',
            'tags': [
                'list:strings'
            ],
            'metrics': {
                'counters': [('message', 'dd.key')],
                'gauges': [("Too high!", "too_high", "<extras.key.path>"),],
            },
            'options': {
                'statsd_host': 'localhost',
                'statsd_port': 8125,
                'local': True,
            }
        }
        expected = {
            'metrics': {
                'c_mapper': {
                    'message': 'dd.key'
                },
                'g_mapper': {
                    'Too high!': {
                        'name': 'too_high',
                        'value': '<extras.key.path>'
                    }
                }
            },
            'name': 'cool',
            'options': {'local': True, 'statsd_host': 'localhost',
            'statsd_port': 8125},
            'tags': ['list:strings']
        }

        dw_config(configs)

        self.assertEquals(_get_config(), expected)

    def test_07_config_bad_dd(self):
        _reset()
        # assert no api key
        configs = {
            'name': 'cool'
        }
        with self.assertRaises(Exception) as e:
            dw_config(configs)
        self.assertEquals(e.exception.message, "Please provide DataDog API Key")

        # assert no app key
        configs = {
            'name': 'cool',
            'options': {
                'api_key': 'neat'
            }
        }
        with self.assertRaises(Exception) as e:
            dw_config(configs)
        self.assertEquals(e.exception.message, "Please provide DataDog APP Key")

    def test_08_config_dd(self):
        _reset()
        configs = {
            'name': 'cool',
            'options': {
                'api_key': 'neat',
                'app_key': 'neat2',
            }
        }
        dw_config(configs)

    def test_09_config_already_init(self):
        configs = {
            'name': 'cool',
            'tags': [
                'list:strings'
            ],
            'metrics': {
                'counters': [('message', 'dd.key')],
                'gauges': [("Too high!", "too_high", "<extras.key.path>"),],
            },
            'options': {
                'statsd_host': 'localhost',
                'statsd_port': 8125,
                'local': True,
            }
        }

        dw_config(configs)
        dw_config(configs)

    @patch('dog_whistle._gauge')
    def test_10_callback_guage(self, g):
        _reset()
        configs = {
            'name': 'cool2',
            'tags': [
                'list:strings'
            ],
            'metrics': {
                'counters': [('message', 'dd.key')],
                'gauges': [("some log", "some_log", "key.key2"),],
            },
            'options': {
                'statsd_host': 'localhost',
                'statsd_port': 8125,
                'local': True,
            }
        }
        dw_config(configs)

        extras = {'key': {'key2': 41}}
        dw_callback("some log", extras)

        g.assert_called_once_with('cool2.some_log', 41, tags=['list:strings'])

    @patch('dog_whistle._gauge')
    def test_11_callback_guage_no_val(self, g):
        _reset()
        configs = {
            'name': 'cool2',
            'tags': [
                'list:strings'
            ],
            'metrics': {
                'counters': [('message', 'dd.key')],
                'gauges': [("some log", "some_log", "key.key2.crazy"),],
            },
            'options': {
                'statsd_host': 'localhost',
                'statsd_port': 8125,
                'local': True,
            }
        }
        dw_config(configs)

        extras = {'key': {'key2': 41}}
        dw_callback("some log", extras)

        g.assert_not_called()

    @patch('dog_whistle._increment')
    def test_12_callback_counter_mapping(self, i):
        _reset()
        configs = {
            'name': 'cool2',
            'tags': [
                'list:strings'
            ],
            'metrics': {
                'counters': [('message', 'dd.key')],
                'gauges': [("some log", "some_log", "key.key2.crazy"),],
            },
            'options': {
                'statsd_host': 'localhost',
                'statsd_port': 8125,
                'local': True,
            }
        }
        dw_config(configs)

        dw_callback("message", {})

        i.assert_called_once_with('cool2.dd.key', tags=['list:strings'])

    @patch('dog_whistle._increment')
    def test_13_callback_counter(self, i):
        _reset()
        configs = {
            'name': 'cool3',
            'options': {
                'statsd_host': 'localhost',
                'statsd_port': 8125,
                'local': True,
            }
        }
        dw_config(configs)

        dw_callback("message", {})

        i.assert_called_once_with('cool3.message', tags=[])

    @patch('dog_whistle._increment')
    def test_14_not_init(self, i):
        _reset()
        configs = {
            'name': 'cool3',
            'options': {
                'statsd_host': 'localhost',
                'statsd_port': 8125,
                'local': True,
            }
        }
        dw_callback("message", {})

        i.assert_not_called()
