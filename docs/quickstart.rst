Quick Start Guide
=================

This guide will help you get started with ARSP quickly.

Running Your First Simulation
------------------------------

1. **Check platform information**::

    arsp info

2. **Run a basic encryption simulation**::

    arsp simulate --scenario encryption --sandbox --monitor

   This will:
   
   * Create an isolated sandbox environment
   * Populate it with test files
   * Execute the encryption scenario
   * Monitor system and file operations
   * Display results

3. **Save simulation results**::

    arsp simulate --scenario encryption --sandbox --output results.json

Analyzing Results
-----------------

After running a simulation, analyze the results::

    arsp analyze results.json

This will:

* Identify behavioral patterns
* Assess risk levels
* Extract Indicators of Compromise (IOCs)
* Generate security recommendations

Save analysis output::

    arsp analyze results.json --output analysis.json --format json

Generating Reports
------------------

Create comprehensive reports::

    # HTML report (recommended)
    arsp report results.json --format html

    # Text report
    arsp report results.json --format text

    # Include analysis
    arsp report results.json --analysis analysis.json --format html

Available Scenarios
-------------------

ARSP provides several pre-built scenarios:

1. **Encryption**: Simulates file encryption behavior
   
   * File enumeration
   * Encryption operations
   * Ransom note creation

2. **Exfiltration**: Simulates data exfiltration
   
   * Sensitive file identification
   * Data staging
   * Exfiltration simulation

3. **Full Attack Chain**: Complete attack simulation
   
   * System enumeration
   * Persistence establishment
   * Data exfiltration
   * File encryption
   * Ransom demand

Example: Full Workflow
----------------------

Complete workflow example::

    # 1. Run simulation
    arsp simulate --scenario full-chain --sandbox --monitor --output sim_results.json

    # 2. Analyze results
    arsp analyze sim_results.json --output analysis.json

    # 3. Generate HTML report
    arsp report sim_results.json --analysis analysis.json --format html

Configuration
-------------

Use a custom configuration file::

    arsp --config my_config.yaml simulate --scenario encryption

Or set environment variables in `.env` file.

Next Steps
----------

* Learn about :doc:`scenarios`
* Understand :doc:`security` guidelines
* Explore the :doc:`api` documentation
