Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-mcp4728/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/mcp4728/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_MCP4728/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_MCP4728/actions
    :alt: Build Status

Helper library for the MCP4728 I2C 12-bit Quad DAC


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_.

Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-mcp4728/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-mcp4728

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-mcp4728

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-mcp4728

Usage Example
=============

.. code-block:: python3

    import board
    import adafruit_mcp4728

    i2c = board.I2C()   # uses board.SCL and board.SDA
    mcp4728 =  adafruit_mcp4728.MCP4728(i2c)

    mcp4728.channel_a.value = 65535 # Voltage = VDD
    mcp4728.channel_b.value = int(65535/2) # VDD/2
    mcp4728.channel_c.value = int(65535/4) # VDD/4
    mcp4728.channel_d.value = 0 # 0V


    mcp4728.save_settings() # save the current values to the eeprom,making them the default on power up


Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/mcp4728/en/latest/>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_MCP4728/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
