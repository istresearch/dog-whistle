logger = LogFactory.get_instance()

logger.info("hey this is a message")

logger.warn("stuff", extras)

logger.info("bad" + str(val), extras)

logger.info("good format stuff here")

logger.warn("bad formatting here {}".format(url))

