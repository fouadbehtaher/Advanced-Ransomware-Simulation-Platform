"""
System monitoring for tracking resource usage and process behavior

Monitors CPU, memory, disk I/O, and network activity during simulations.
"""
from typing import Dict, Any, List, Optional
import psutil
import time
from datetime import datetime
from threading import Thread, Event

from arsp.core.config import Config
from arsp.core.logger import Logger


class SystemMonitor:
    """Monitor system resources during ransomware simulations"""
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize system monitor
        
        Args:
            config: Optional configuration object
        """
        self.config = config or Config()
        self.logger = Logger().get_logger(
            "system_monitor",
            self.config.get("monitoring.log_level", "INFO"),
            self.config.get("monitoring.log_path")
        )
        
        self._monitoring = False
        self._monitor_thread: Optional[Thread] = None
        self._stop_event = Event()
        self._metrics: List[Dict[str, Any]] = []
        self._interval = 1.0  # seconds
    
    def start(self, interval: float = 1.0) -> None:
        """
        Start monitoring system resources
        
        Args:
            interval: Monitoring interval in seconds
        """
        if self._monitoring:
            self.logger.warning("Monitor already running")
            return
        
        self._interval = interval
        self._monitoring = True
        self._stop_event.clear()
        self._metrics = []
        
        self._monitor_thread = Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
        
        self.logger.info(f"System monitoring started (interval: {interval}s)")
    
    def stop(self) -> None:
        """Stop monitoring system resources"""
        if not self._monitoring:
            return
        
        self._monitoring = False
        self._stop_event.set()
        
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5)
        
        self.logger.info("System monitoring stopped")
    
    def _monitor_loop(self) -> None:
        """Main monitoring loop"""
        while self._monitoring and not self._stop_event.is_set():
            try:
                metrics = self._collect_metrics()
                self._metrics.append(metrics)
            except Exception as e:
                self.logger.error(f"Error collecting metrics: {str(e)}")
            
            time.sleep(self._interval)
    
    def _collect_metrics(self) -> Dict[str, Any]:
        """Collect current system metrics"""
        return {
            "timestamp": datetime.now().isoformat(),
            "cpu": {
                "percent": psutil.cpu_percent(interval=0.1),
                "count": psutil.cpu_count(),
            },
            "memory": {
                "percent": psutil.virtual_memory().percent,
                "available_mb": psutil.virtual_memory().available / (1024 * 1024),
                "used_mb": psutil.virtual_memory().used / (1024 * 1024),
            },
            "disk": {
                "read_bytes": psutil.disk_io_counters().read_bytes if psutil.disk_io_counters() else 0,
                "write_bytes": psutil.disk_io_counters().write_bytes if psutil.disk_io_counters() else 0,
            },
            "network": {
                "bytes_sent": psutil.net_io_counters().bytes_sent,
                "bytes_recv": psutil.net_io_counters().bytes_recv,
            } if psutil.net_io_counters() else {},
        }
    
    def get_metrics(self) -> List[Dict[str, Any]]:
        """Get collected metrics"""
        return self._metrics.copy()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics of collected metrics"""
        if not self._metrics:
            return {}
        
        cpu_values = [m["cpu"]["percent"] for m in self._metrics]
        memory_values = [m["memory"]["percent"] for m in self._metrics]
        
        return {
            "duration_seconds": len(self._metrics) * self._interval,
            "samples_collected": len(self._metrics),
            "cpu": {
                "avg": sum(cpu_values) / len(cpu_values),
                "max": max(cpu_values),
                "min": min(cpu_values),
            },
            "memory": {
                "avg": sum(memory_values) / len(memory_values),
                "max": max(memory_values),
                "min": min(memory_values),
            },
        }
    
    def clear_metrics(self) -> None:
        """Clear collected metrics"""
        self._metrics = []
        self.logger.debug("Metrics cleared")
