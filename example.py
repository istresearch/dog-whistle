from scutils.log_factory import LogFactory
import random
import logging
from random import randrange
from time import sleep

logger = logging.getLogger('dog_whistle')
# logger.setLevel(logging.DEBUG)
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')
# ch.setFormatter(formatter)
# logger.addHandler(ch)

#logger = logging.getLogger('datadog.api')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


from dog_whistle import dw_config, dw_callback


settings = {
    'name': 'Scrapy Cluster',
    'tags': [
        # high level tags that everything in your app will have
        'list:strings'
    ],
    'metrics': {

    },
    'options': {
        # use statsd for local testing, see docs
        'statsd_host': 'localhost',
        'statsd_port': 8125,
        'local': True,
        # OR
        # # use datadog for DD integration
        # 'api_key': 'KEY',
        # 'app_key': 'OTHER_KEY',
        # 'api_host': 'localhost',
    }
}

dw_config(settings)

# from datadog import statsd
# from datadog import initialize
# initialize(**settings['options'])
# statsd.increment('scrapy_cluster.test')
# statsd.gauge('scrapy_cluster.gauge', 42)
# from datadog import ThreadStats
# stats = ThreadStats()
# stats.start()
# stats.increment('scrapy_cluster.thread_stats.hits')

logger = LogFactory.get_instance(level='INFO')
logger.register_callback('*', dw_callback)

for i in xrange(0, 10):
    logger.info("this is a test")

val = 50
for i in xrange(0, 10):
    val += randrange(-1, 2, 1)
    logger.info("I have a guage and this message is really long and stuff", {'value': i})
    #logger.warn("bad line " + str(val))

    if val > 50:
        logger.error("Too high!", {'wrapper': {'value': val}})
