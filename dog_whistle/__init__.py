# Set default logging handler to avoid "No handler found" warnings.
import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

import os
import re
import copy

logging.getLogger(__name__).addHandler(NullHandler())
log = logging.getLogger(__name__)

_dw_configuration = None
_dw_thread_stats = None
_dw_init = False
_dw_stats = None
_dw_local = False


def dw_analyze(path):
    """Used to analyze a project structure and output the recommended
    settings dictionary to be used when used in practice. Run this method, then
    add the resulting output to your project

    :param str path: The folder path to analyze
    """
    log.debug("dw_analyze")

    def walk(path):
        """Walks a directory, yields filepaths"""
        for dirName, subdirList, fileList in os.walk(path):
            log.debug('Found directory: %s' % dirName)
            for fname in fileList:
                log.debug('File: \t%s' % fname)
                val = os.path.join(dirName, fname)
                yield val

    # compile regexes
    regex_lf = re.compile('(LogFactory.get_instance)')
    regex_log = re.compile('\.(?:info|warn|warning|error|critical)\((\".*\").*\)')
    regex_inc = re.compile('\.(?:info|warn|warning|error|critical)\((.*(?:\+|format).*).*\)')
    regex_com = re.compile('\".*\"\,')
    found_lf = False
    line_cache = []
    unknown_cache = []

    for file in walk(path):
        log.debug("checking file " + file)

        with open(file, 'r') as f:
            line_number = 1

            for line in f:
                results = regex_lf.findall(line)
                if len(results) > 0:
                    log.debug("found log factory use")
                    found_lf = True

                matches = regex_log.findall(line)
                if len(matches) > 0:
                    if len(regex_inc.findall(line)) == 0:
                        log.debug("found valid line")
                        line_cache.append((file, line_number, line.strip(), matches[0]))
                    else:
                        log.debug("found unknown line")
                        unknown_cache.append((file, line_number, line.strip(), matches[0]))

                line_number += 1

    if found_lf:
        log.debug("LogFactory in use")
        print ""
        print "Valid Lines"
        print "-----------"
        curr_file = None
        for item in line_cache:
            if curr_file != item[0]:
                curr_file = item[0]
                print item[0]
            print '  ', item[1], ':', item[2]

        print ""
        print "Invalid Lines"
        print "-------------"
        curr_file = None
        for item in unknown_cache:
            if curr_file != item[0]:
                curr_file = item[0]
                print item[0]
            print '  ', item[1], ':', item[2]

        # messy but it makes a really nice string in the end
        recommended_str = '''
dw_dict = {
    'tags': [
        # high level tags that everything in your app will have
        'item:descriptor'
    ],
    'metrics': {
        'counters': [
            # datadog metrics that will use ++'''

        for item in line_cache:
            if len(regex_com.findall(item[2])) == 0:
                recommended_str += '\n            (' + item[3] + ', "<datadog.metric>"),'

        recommended_str += '''
        ],
        'guages': [
            # datadog metrics that have a predefined value like `51`'''

        for item in line_cache:
            if len(regex_com.findall(item[2])) > 0:
                recommended_str += '\n            (' + item[3] + ', "<datadog.metric>", "<extras.key.path>"),'

        recommended_str += '''
        ]
    },
    'options': {
        # use statsd for local testing, see docs
        'statsd_host': 'localhost',
        'local': True,
        # OR use datadog for DD integration
        'api_key': 'abc123',
        'app_key': 'key',
        'api_host': 'ddhost',
    },

}

Ensure the above dictionary is passed into `dw_config()`
'''

        print ""
        print "Generated Template Settings"
        print "---------------------------"
        print recommended_str


def dw_config(settings):
    """Set up the datadog callback integration

    :param dict settings: The settings dict containing the `analyze()`
    configuration
    """
    # import globals
    global _dw_configuration
    global _dw_thread_stats
    global _dw_init
    global _dw_stats
    global _dw_local

    log.debug("dw_config called")

    if not _dw_init:
        _dw_configuration = settings
        log.debug("init settings " + str(_dw_configuration))
        # check configuration validity
        # stuff

        if 'local' in _dw_configuration['options'] and _dw_configuration['options']['local'] == True:
            from statsd import StatsClient
            statsd = StatsClient(_dw_configuration['options']['statsd_host'],
                                 _dw_configuration['options']['statsd_port'])
            _dw_stats = statsd
            _dw_stats.increment = statsd.incr
            _dw_local = True
        else:
            from datadog import initialize, ThreadStats
            initialize(**_dw_configuration['options'])
            _dw_stats = ThreadStats()
            _dw_stats.start()

        _dw_configuration['metrics']['c_mapper'] = {}
        _dw_configuration['metrics']['g_mapper'] = {}

        for item in _dw_configuration['metrics']['counters']:
            _dw_configuration['metrics']['c_mapper'][item[0]] = item[1]

        for item in _dw_configuration['metrics']['guages']:
            _dw_configuration['metrics']['g_mapper'][item[0]] = {
                'name': item[1],
                'value': item[2]
            }
        del _dw_configuration['metrics']['guages']
        del _dw_configuration['metrics']['counters']

        _dw_init = True
    else:
        log.warning("tried to configure DogWatcher more than once within app")


def dw_callback(message, extras):
    """The actual callback method passed to the logger

    :param str message: The log message
    :param dict extras: The extras dictionary from the logger
    """
    # import globals
    global _dw_configuration
    global _dw_init
    global _dw_thread_stats
    log.debug("dw_callback called")

    if _dw_init:
        log.debug("inside callback " + message + " " + str(extras))
        # increment counter metric
        if message in _dw_configuration['metrics']['c_mapper']:
            log.info("incremented counter")
            _increment(_dw_configuration['metrics']['c_mapper'][message],
                       tags=_dw_configuration['tags'])

        # set guage metric
        if message in _dw_configuration['metrics']['g_mapper']:
            value = _get_value(extras,
                               _dw_configuration['metrics']['g_mapper'][message]['value'])
            if value is None:
                log.warning("Could not find key inside extras")
            else:
                log.info("metric guage")
                _gauge(_dw_configuration['metrics']['g_mapper'][message]['name'],
                       value, tags=_dw_configuration['tags'])

    else:
        log.warning("Tried to increment attribute before configuration")


def _get_value(item, key):
    """Grabs a nested value within a dict

    :param dict item: the dictionary
    :param str key: the nested key to find
    :returns: the value if found, otherwise None
    """
    keys = key.split('.', 1)

    if isinstance(item, dict):
        if len(keys) == 2:
            if keys[0] in item:
                return _get_value(item[keys[0]], keys[1])
        elif keys[0] in item:
            return copy.deepcopy(item[keys[0]])


def _increment(name, tags):
    """Increments a counter

    :param str name: The name of the stats
    :param list tag: A list of tags"""
    global _dw_stats
    global _dw_local

    if _dw_local:
        _dw_stats.increment(name)
    else:
        _dw_stats.increment(name, tag)


def _gauge(name, value, tags):
    """Increments a gauge

    :param str name: The name of the stats
    :param int value: The value of the gauge
    :param list tag: A list of tags"""
    global _dw_stats
    global _dw_local

    if _dw_local:
        _dw_stats.gauge(name, value)
    else:
        _dw_stats.gauge(name, value, tags)
