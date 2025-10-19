"""Common test fixtures and utilities"""
import pytest
import tempfile
import shutil
from pathlib import Path

from arsp.core.config import Config


@pytest.fixture
def temp_dir():
    """Create temporary directory for tests"""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    # Cleanup
    if temp_path.exists():
        shutil.rmtree(temp_path)


@pytest.fixture
def test_config():
    """Create test configuration"""
    config = Config()
    config.set("simulation.sandbox_path", "/tmp/arsp_test_sandbox")
    config.set("monitoring.log_level", "DEBUG")
    return config


@pytest.fixture
def sample_simulation_results():
    """Sample simulation results for testing"""
    return {
        "scenario_name": "Test Encryption",
        "scenario_type": "encryption",
        "status": "completed",
        "duration_seconds": 5.5,
        "steps": [
            {
                "name": "enumerate_files",
                "action": "enumerate",
                "status": "success",
                "duration_seconds": 1.0
            },
            {
                "name": "encrypt_files",
                "action": "encrypt",
                "status": "success",
                "duration_seconds": 3.0
            },
            {
                "name": "create_ransom_note",
                "action": "create_note",
                "status": "success",
                "duration_seconds": 0.5
            }
        ],
        "metrics": {
            "files_processed": 10,
            "files_encrypted": 10,
            "bytes_processed": 1024000
        }
    }
