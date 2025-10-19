"""
Sandbox isolation for secure simulation execution

Provides isolated environment for running ransomware simulations safely.
"""
from typing import Optional, Dict, Any, List
from pathlib import Path
import os
import shutil
from datetime import datetime

from arsp.core.config import Config
from arsp.core.logger import Logger


class Sandbox:
    """Isolated sandbox environment for simulations"""
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize sandbox
        
        Args:
            config: Optional configuration object
        """
        self.config = config or Config()
        self.logger = Logger().get_logger(
            "sandbox",
            self.config.get("monitoring.log_level", "INFO"),
            self.config.get("monitoring.log_path")
        )
        
        self.sandbox_path: Optional[Path] = None
        self.is_active = False
        self._original_files: List[str] = []
    
    def create(self, name: Optional[str] = None) -> Path:
        """
        Create sandbox environment
        
        Args:
            name: Optional sandbox name
            
        Returns:
            Path to sandbox directory
        """
        if self.is_active:
            self.logger.warning("Sandbox already active")
            return self.sandbox_path
        
        base_path = Path(self.config.get("simulation.sandbox_path"))
        
        if name:
            self.sandbox_path = base_path / name
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.sandbox_path = base_path / f"sandbox_{timestamp}"
        
        self.sandbox_path.mkdir(parents=True, exist_ok=True)
        self.is_active = True
        
        self.logger.info(f"Sandbox created: {self.sandbox_path}")
        return self.sandbox_path
    
    def populate(self, sample_files: Optional[List[str]] = None) -> None:
        """
        Populate sandbox with test files
        
        Args:
            sample_files: Optional list of file paths to copy into sandbox
        """
        if not self.is_active or not self.sandbox_path:
            raise RuntimeError("Sandbox not active")
        
        if sample_files:
            for file_path in sample_files:
                src = Path(file_path)
                if src.exists() and src.is_file():
                    dst = self.sandbox_path / src.name
                    shutil.copy2(src, dst)
                    self._original_files.append(str(dst))
                    self.logger.debug(f"Copied file to sandbox: {src.name}")
        else:
            # Create default test files
            self._create_default_files()
    
    def _create_default_files(self) -> None:
        """Create default test files in sandbox"""
        default_files = [
            ("test_document.txt", "This is a test document for simulation."),
            ("sample_data.txt", "Sample data file with some content."),
            ("important_file.txt", "Important file for testing encryption."),
        ]
        
        for filename, content in default_files:
            file_path = self.sandbox_path / filename
            file_path.write_text(content)
            self._original_files.append(str(file_path))
            self.logger.debug(f"Created default file: {filename}")
    
    def cleanup(self, remove_all: bool = False) -> None:
        """
        Cleanup sandbox environment
        
        Args:
            remove_all: If True, remove entire sandbox directory
        """
        if not self.is_active or not self.sandbox_path:
            return
        
        try:
            if remove_all and self.sandbox_path.exists():
                shutil.rmtree(self.sandbox_path)
                self.logger.info(f"Sandbox removed: {self.sandbox_path}")
            else:
                # Just clean up modified files, keep originals
                for item in self.sandbox_path.iterdir():
                    if str(item) not in self._original_files:
                        if item.is_file():
                            item.unlink()
                        elif item.is_dir():
                            shutil.rmtree(item)
                self.logger.info("Sandbox cleaned up")
        
        except Exception as e:
            self.logger.error(f"Error cleaning up sandbox: {str(e)}")
        
        finally:
            self.is_active = False
            self._original_files = []
    
    def get_path(self) -> Optional[Path]:
        """Get sandbox path"""
        return self.sandbox_path
    
    def get_info(self) -> Dict[str, Any]:
        """Get sandbox information"""
        if not self.sandbox_path or not self.sandbox_path.exists():
            return {}
        
        total_size = sum(
            f.stat().st_size 
            for f in self.sandbox_path.rglob('*') 
            if f.is_file()
        )
        
        file_count = sum(1 for _ in self.sandbox_path.rglob('*') if _.is_file())
        
        return {
            "path": str(self.sandbox_path),
            "is_active": self.is_active,
            "file_count": file_count,
            "total_size_bytes": total_size,
            "created_files": len(self._original_files),
        }
