Installation Guide
==================

Requirements
------------

* Python 3.8 or higher
* pip package manager
* Virtual environment (recommended)

Installation Steps
------------------

1. Clone the repository::

    git clone https://github.com/fouadbehtaher/Advanced-Ransomware-Simulation-Platform.git
    cd Advanced-Ransomware-Simulation-Platform

2. Create a virtual environment::

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\\Scripts\\activate

3. Install dependencies::

    pip install -r requirements.txt

4. Install ARSP in development mode::

    pip install -e .

5. Verify installation::

    arsp --version
    arsp info

Configuration
-------------

Copy the example environment file::

    cp .env.example .env

Edit `.env` to customize your configuration:

* **SIMULATION_MODE**: Set to `isolated` for sandbox execution
* **SANDBOX_PATH**: Directory for sandbox environment
* **LOG_LEVEL**: Logging verbosity (DEBUG, INFO, WARNING, ERROR)
* **ENABLE_NETWORK_ISOLATION**: Enable network isolation (true/false)

Development Installation
------------------------

For development with additional tools::

    pip install -r requirements.txt
    pip install -e .[dev]

This includes testing, linting, and documentation tools.
