logger = LogFactory.get_instance()

logger.info("hey this is a message")

logger.warn("stuff", extras)

logger.info("bad" + str(val), extras)
