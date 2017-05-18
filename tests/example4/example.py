logger = LogFactory.get_instance()

logger.info('this is a test', extra={'foo': 'bar'})
logger.warn('This is another "test"', extra={'foo': "bar", 'bar': "baz", "lorem": "ipsum"})

