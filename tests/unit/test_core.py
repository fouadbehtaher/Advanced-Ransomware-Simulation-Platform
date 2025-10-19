"""Test suite for ARSP core functionality"""
import pytest
from arsp.core.config import Config
from arsp.core.logger import Logger


class TestConfig:
    """Test configuration management"""
    
    def test_config_initialization(self):
        """Test basic config initialization"""
        config = Config()
        assert config is not None
        assert config.get("simulation.mode") is not None
    
    def test_config_get(self):
        """Test getting configuration values"""
        config = Config()
        mode = config.get("simulation.mode")
        assert mode in ["isolated", "controlled"]
    
    def test_config_set(self):
        """Test setting configuration values"""
        config = Config()
        config.set("test.value", "test123")
        assert config.get("test.value") == "test123"
    
    def test_config_default(self):
        """Test default values"""
        config = Config()
        assert config.get("nonexistent.key", "default") == "default"


class TestLogger:
    """Test logging functionality"""
    
    def test_logger_initialization(self):
        """Test logger initialization"""
        logger_manager = Logger()
        logger = logger_manager.get_logger("test")
        assert logger is not None
    
    def test_logger_singleton(self):
        """Test logger singleton pattern"""
        logger1 = Logger()
        logger2 = Logger()
        assert logger1 is logger2
    
    def test_logger_levels(self):
        """Test different log levels"""
        logger_manager = Logger()
        
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            logger = logger_manager.get_logger(f"test_{level}", level)
            assert logger is not None
