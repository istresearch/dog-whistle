Usage
=====

This section outlines how to use the ``dog_whistle`` library in your project.

Analyze
-------

The first step you need to do is to download the ``dog_whistle`` library from pip.

::

    pip install dog-whistle

.. note:: You must be connected to the IST Research Pip repo in order to install dog-whistle, as it is currently not open source

Navigate to the root directory of your project or code base, and run the following commands in the python shell:

::

    $ python
    >>> from dog_whistle import dw_analyze
    >>> dw_analyze('./')
    # it will spit out a bunch of text, like below:

    Valid Lines
    -----------
    ./crawling/distributed_scheduler.py
       111 : self.logger.error("Could not connect to Zookeeper")
       117 : self.logger.error("Could not ping Zookeeper")
       131 : self.logger.info("Zookeeper config changed", extra=loaded_config)
       189 : self.logger.info("Lost config from Zookeeper", extra=extras)
       303 : self.logger.error("Could not reach out to get public ip")
       381 : self.logger.info("Closing Spider", {'spiderid':self.spider.name})
       383 : self.logger.warning("Clearing crawl queues")

    Invalid Lines
    -------------

    <<<<<<<<<< YOU MUST FIX THESE BEFORE USING THE DOGWHISTLE LIBRARY >>>>>>>>>>>

    ./crawling/spiders/wandering_spider.py
       87 : self._logger.info("Did not find any more links" + str(value))


    Auto-Generated Template Settings
    --------------------------------

    dw_dict = {
        'name': '<my_project>',
        'tags': [
            # high level tags that everything in your app will have
            'item:descriptor'
        ],
        'metrics': {
            # By default, everything is a counter using the concatentated log string
            # the 'counters' key is NOT required, it is shown here for illustration
            'counters': [
                # datadog metrics that will use ++
                ("Could not connect to Zookeeper", "could_not_connect_to_zookeeper"),
                ("Could not ping Zookeeper", "could_not_ping_zookeeper"),
                ("Zookeeper config changed", "zookeeper_config_changed"),
                ("Lost config from Zookeeper", "lost_config_from_zookeeper"),
            ],
            # datadog metrics that have a predefined value like `51`
            # These metrics override any 'counter' with the same key,
            # and are shown here for illustration purposes only
            'gauges': [

                ("Zookeeper config changed", "zookeeper_config_changed", "<extras.key.path>"),
                ("Lost config from Zookeeper", "lost_config_from_zookeeper", "<extras.key.path>"),
            ]
        },
        'options': {
            # use statsd for local testing, see docs
            'statsd_host': 'localhost',
            'statsd_port': 8125,
            'local': True,
        },

    }

    Ensure the above dictionary is passed into `dw_config()`

    >>>

Lets break down each of these sections in more detail.

**Valid Lines**

This section outlines the valid logger lines that dog whistle has detected will work without issue. They should represent 'static' messages, and not include any variable substitution within the log message itself.

**Invalid Lines**

These lines were noted to have some kind of variable substitution inside them, and need to be corrected before being used by the dog whistle module. All variables *should* be enclosed in the ``extras`` dictionary anyways, and this helps standardize our logging practices.

.. warning:: You **must** correct these lines before using the dog whistle in production, otherwise our datadog metrics will not be consistent


**Auto-Generated Template Settings**

By analyzing only your valid lines, the dog whistle library dumps out a dictionary object that you will need to tweak and use later. At a bare minimum, it requires the following key:

* **name** - the name of your overall project

If you do not provide an ``options`` key, it is assumed you will be passing your ``DATADOG_API_KEY`` and ``DATADOG_APP_KEY`` via environment variables.


* **options** - the options to be passed to configure the statsd or datadog setup

For example:

::

    {
        'name': 'cool project',
        'options': {
            'statsd_host': 'localhost',
            'statsd_port': 8125,
            'local': True,
        }
    }

This configures all log messages to be counters, tied to the ``cool project`` namespace, and configured to use a local statsd host.

Further configuration can be refined via the ``metrics`` key, allow you to specify custom mappings of *log messages* to *keys*.

::

    'counters': [
        ("Could not connect to Zookeeper", "zookeeper.connection.error"),
        ("Could not ping Zookeeper", "zookeeper.connection.ping"),
        ("Zookeeper config changed", "zookeeper.config_changed"),
        ("Lost config from Zookeeper", "lost_config_from_zookeeper"),
    ],

Normally, the dog whistle sanitizes the log message into a lowercase/underscore form. However, we also provide the ability to custom map log messages to key naming conventions.

In the above example, we see a ``counters`` mapping being applied to three of the four log messages. Instead of using the default (shown on line 4), it will use the custom key.

The same can be said for gauges:

::

    'gauges': [
        ("Zookeeper config changed", "zookeeper_config_changed", "buried.key.here"),
        ("Lost config from Zookeeper", "zookeeper.connection.problem", "num_tries"),
    ]

The dog whistle library automatically detects ``extras`` being passed into the log method, and adds lines here to recommend you use a gauge incase you are tracking a particular value in question via your ``extras`` dictionary.

.. note:: At time of writing, dog whistle does not support multiple gauges for a single log statement

Here, we dig into the extras dictionary using dot notation to try to find the value we are looking for. If no value is found, it is not sent.

Lastly, ``tags`` are something that will always be included in your datadog stats. Here, you can specify a unique descriptor or other item to identify your process from the rest of the group. These tags are optional, but are helpful.

Local Configuration
-------------------

Setup
^^^^^

Now that you have an idea about your configuration, you need to integrate dog whistle into every python process or application you run. You will need to get the settings dictionary with your proper configuration into your application somehow. This guide does not cover the various ways of including the dictionary, however it is advised that you use either a settings file, environment variables, or some other way to avoid hard coding critical settings into your source code.

Once you have figured that out, at a **single** point within your application, add the following lines of code:

::

    from dog_whistle import dw_config, dw_callback
    settings = {} # your settings here
    dw_config(settings)

This will configue your dog whistle library to be ready to send metrics, the next step is to add a LogFactory ``callback`` like so:

::

    logger = LogFactory.get_instance() # your normal LogFactory setup can go here
    logger.register_callback('*', dw_callback)

.. note:: You will need ``scutils==1.2.0dev7`` or above in order to use the callback feature in your project. Please update your requirements appropriately!

This will allow the dog whistle library to integrate and monitor every call the LogFactory logger creates. The callback system is much more advanced than what is decribed here, but this gives us the ability to monitor all log messages actually written by logger, anything ignored by the logger will also be ignored by this callback.

Testing
^^^^^^^

Let's test our configuration using a simple `statsd <https://github.com/etsy/statsd>`_ + `graphite <http://graphite.readthedocs.io/>`_ host. Here, we are going to use Docker to pull a container that allows us to view our new metrics to check naming conventions, typos, and other things.

::

    $ docker run --restart=always -p 80:80 -p 2003-2004:2003-2004 -p 2023-2024:2023-2024 -p 8125:8125/udp -p 8126:8126 hopsoft/graphite-statsd

That's it! Run your application with a local setup, specifying the host as ``localhost`` and the port as ``8125``, and your metrics will pump into the container running.

You can visit ``localhost:80`` to view your Graphite dashboard. On the ``Tree`` on the left hand side, navigate to ``Metrics/stats``. You should see your project name as a folder, and you can click on the individual metric to get it to show up in the graph.

.. note:: The graph comes by default with a 24hr view, click the "clock" icon on the graph to change it to minutes, otherwise you may not be able to see your data!

The same thing can be done under the ``Metrics/stats/gauges`` folder, you should see your project name and be able to click on any gauge metrics you would like.

< INSERT PICTURE HERE >

If you are happy with your setup, this completes the local testing of the dog whistle integration into your project.

Datadog Configuration
---------------------

TODO

Wrapping Up
-----------

Be sure to add the following to your projects requirements.txt!

::

    dog-whistle==X.X
    scutils==1.2.0dev7

Where ``X.X`` is the current version of ``dog-whistle`` on pypi

.. note:: Version numbers are subject to change!