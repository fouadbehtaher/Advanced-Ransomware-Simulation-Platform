"""
File system monitoring for tracking file operations

Monitors file creation, modification, deletion, and encryption activities.
"""
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

from arsp.core.config import Config
from arsp.core.logger import Logger


class FileEventHandler(FileSystemEventHandler):
    """Custom file system event handler"""
    
    def __init__(self, callback: Callable[[FileSystemEvent], None]):
        """
        Initialize event handler
        
        Args:
            callback: Callback function to handle events
        """
        super().__init__()
        self.callback = callback
    
    def on_any_event(self, event: FileSystemEvent) -> None:
        """Handle any file system event"""
        if not event.is_directory:
            self.callback(event)


class FileMonitor:
    """Monitor file system operations during simulations"""
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize file monitor
        
        Args:
            config: Optional configuration object
        """
        self.config = config or Config()
        self.logger = Logger().get_logger(
            "file_monitor",
            self.config.get("monitoring.log_level", "INFO"),
            self.config.get("monitoring.log_path")
        )
        
        self._observer: Optional[Observer] = None
        self._monitoring = False
        self._events: List[Dict[str, Any]] = []
        self._watch_path: Optional[str] = None
    
    def start(self, watch_path: str) -> None:
        """
        Start monitoring file system
        
        Args:
            watch_path: Path to monitor
        """
        if self._monitoring:
            self.logger.warning("File monitor already running")
            return
        
        self._watch_path = watch_path
        path = Path(watch_path)
        
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        
        self._observer = Observer()
        event_handler = FileEventHandler(self._handle_event)
        self._observer.schedule(event_handler, str(path), recursive=True)
        self._observer.start()
        
        self._monitoring = True
        self._events = []
        
        self.logger.info(f"File monitoring started for: {watch_path}")
    
    def stop(self) -> None:
        """Stop monitoring file system"""
        if not self._monitoring or not self._observer:
            return
        
        self._observer.stop()
        self._observer.join(timeout=5)
        
        self._monitoring = False
        self.logger.info("File monitoring stopped")
    
    def _handle_event(self, event: FileSystemEvent) -> None:
        """
        Handle file system event
        
        Args:
            event: File system event
        """
        event_data = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event.event_type,
            "src_path": event.src_path,
            "is_directory": event.is_directory,
        }
        
        if hasattr(event, 'dest_path'):
            event_data["dest_path"] = event.dest_path
        
        self._events.append(event_data)
        
        self.logger.debug(
            f"File event: {event.event_type} - {Path(event.src_path).name}"
        )
    
    def get_events(self) -> List[Dict[str, Any]]:
        """Get all recorded file events"""
        return self._events.copy()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of file operations"""
        if not self._events:
            return {}
        
        event_types = {}
        for event in self._events:
            event_type = event["event_type"]
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        return {
            "watch_path": self._watch_path,
            "total_events": len(self._events),
            "event_breakdown": event_types,
            "unique_files": len(set(e["src_path"] for e in self._events)),
        }
    
    def clear_events(self) -> None:
        """Clear recorded events"""
        self._events = []
        self.logger.debug("Events cleared")
    
    def is_monitoring(self) -> bool:
        """Check if monitoring is active"""
        return self._monitoring
