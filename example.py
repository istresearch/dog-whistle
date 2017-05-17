from scutils.log_factory import LogFactory
import random
import logging
from random import randrange
from time import sleep

logger = logging.getLogger('dog_whistle')
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
        'gauges': [
            ("Too high!", [
                ("too_high", "wrapper.value"),
                ("too_high_gauge2", "key2"),
            ])
        ]
    },
    'options': {
        # use statsd for local testing, see docs
        'statsd_host': 'localhost',
        'statsd_port': 8125,
        'local': True,

    }
}

dw_config(settings)

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
        logger.error("Too high!", {'wrapper': {'value': val}, 'key2': 11})
