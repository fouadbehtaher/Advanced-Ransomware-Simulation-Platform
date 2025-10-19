"""
Advanced Ransomware Simulation Platform (ARSP)

A secure and isolated framework for executing, monitoring, and analyzing 
advanced ransomware behaviors for security testing and training purposes.

Author: ARSP Development Team
License: MIT
Version: 0.1.0
"""

__version__ = "0.1.0"
__author__ = "ARSP Development Team"
__license__ = "MIT"

from arsp.core.config import Config
from arsp.core.logger import Logger

__all__ = ["Config", "Logger", "__version__"]
