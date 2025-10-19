"""
Core configuration module for ARSP

Handles loading and managing configuration from environment variables and files.
"""
import os
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv
import yaml


class Config:
    """Main configuration class for ARSP"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration
        
        Args:
            config_file: Optional path to YAML configuration file
        """
        # Load environment variables
        load_dotenv()
        
        # Default configuration
        self._config: Dict[str, Any] = {
            "simulation": {
                "mode": os.getenv("SIMULATION_MODE", "isolated"),
                "sandbox_path": os.getenv("SANDBOX_PATH", "/tmp/arsp_sandbox"),
                "max_file_size_mb": int(os.getenv("MAX_FILE_SIZE_MB", "100")),
                "timeout_seconds": int(os.getenv("SIMULATION_TIMEOUT_SECONDS", "300")),
            },
            "security": {
                "enable_network_isolation": os.getenv("ENABLE_NETWORK_ISOLATION", "true").lower() == "true",
                "enable_filesystem_isolation": os.getenv("ENABLE_FILESYSTEM_ISOLATION", "true").lower() == "true",
                "enable_process_monitoring": os.getenv("ENABLE_PROCESS_MONITORING", "true").lower() == "true",
                "allowed_operations": os.getenv("ALLOWED_OPERATIONS", "encrypt,decrypt,enumerate,exfiltrate").split(","),
            },
            "monitoring": {
                "log_level": os.getenv("LOG_LEVEL", "INFO"),
                "log_path": os.getenv("LOG_PATH", "./logs"),
                "enable_detailed_logging": os.getenv("ENABLE_DETAILED_LOGGING", "true").lower() == "true",
                "enable_metrics_collection": os.getenv("ENABLE_METRICS_COLLECTION", "true").lower() == "true",
            },
            "analysis": {
                "enable_behavioral_analysis": os.getenv("ENABLE_BEHAVIORAL_ANALYSIS", "true").lower() == "true",
                "enable_static_analysis": os.getenv("ENABLE_STATIC_ANALYSIS", "false").lower() == "true",
                "output_path": os.getenv("ANALYSIS_OUTPUT_PATH", "./analysis_results"),
            },
            "reporting": {
                "format": os.getenv("REPORT_FORMAT", "json"),
                "enable_auto_report": os.getenv("ENABLE_AUTO_REPORT", "true").lower() == "true",
                "output_path": os.getenv("REPORT_OUTPUT_PATH", "./reports"),
            },
            "database": {
                "type": os.getenv("DATABASE_TYPE", "sqlite"),
                "path": os.getenv("DATABASE_PATH", "./data/arsp.db"),
            },
            "api": {
                "enabled": os.getenv("API_ENABLED", "false").lower() == "true",
                "host": os.getenv("API_HOST", "127.0.0.1"),
                "port": int(os.getenv("API_PORT", "8000")),
                "key": os.getenv("API_KEY", ""),
            }
        }
        
        # Load from YAML file if provided
        if config_file and Path(config_file).exists():
            self._load_yaml_config(config_file)
    
    def _load_yaml_config(self, config_file: str) -> None:
        """Load configuration from YAML file"""
        with open(config_file, 'r') as f:
            yaml_config = yaml.safe_load(f)
            if yaml_config:
                self._merge_config(yaml_config)
    
    def _merge_config(self, new_config: Dict[str, Any]) -> None:
        """Merge new configuration with existing"""
        for key, value in new_config.items():
            if key in self._config and isinstance(value, dict):
                self._config[key].update(value)
            else:
                self._config[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key"""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value by dot-notation key"""
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value
    
    @property
    def all(self) -> Dict[str, Any]:
        """Get all configuration"""
        return self._config.copy()
