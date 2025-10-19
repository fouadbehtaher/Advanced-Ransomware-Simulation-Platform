Advanced Ransomware Simulation Platform (ARSP) Documentation
=============================================================

Welcome to the ARSP documentation!

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api
   scenarios
   security

Introduction
------------

ARSP is a secure and isolated framework for executing, monitoring, and analyzing 
advanced ransomware behaviors for security testing and training purposes.

Key Features
------------

* **Isolated Sandbox Environment**: Execute simulations in a controlled, isolated environment
* **Behavioral Analysis**: Analyze and identify ransomware behavior patterns
* **Comprehensive Monitoring**: Track system resources, file operations, and network activity
* **Flexible Scenarios**: Pre-built and custom scenario support
* **Detailed Reporting**: Generate reports in JSON, text, and HTML formats
* **CLI Interface**: Easy-to-use command-line interface

Quick Start
-----------

Installation::

    pip install -e .

Run a basic simulation::

    arsp simulate --scenario encryption --sandbox --monitor

Analyze results::

    arsp analyze results.json

Generate a report::

    arsp report results.json --format html

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
