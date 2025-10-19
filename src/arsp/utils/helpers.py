"""
Helper utilities for ARSP

Common utility functions used across the platform.
"""
from typing import Union


def format_bytes(bytes_value: Union[int, float]) -> str:
    """
    Format bytes into human-readable string
    
    Args:
        bytes_value: Number of bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def format_duration(seconds: Union[int, float]) -> str:
    """
    Format duration in seconds to human-readable string
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted string (e.g., "1h 23m 45s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    
    if minutes < 60:
        return f"{minutes}m {secs}s"
    
    hours = minutes // 60
    minutes = minutes % 60
    
    return f"{hours}h {minutes}m {secs}s"


def validate_path(path: str, must_exist: bool = False) -> bool:
    """
    Validate file system path
    
    Args:
        path: Path to validate
        must_exist: If True, path must exist
        
    Returns:
        True if valid, False otherwise
    """
    from pathlib import Path
    
    try:
        p = Path(path)
        if must_exist:
            return p.exists()
        return True
    except Exception:
        return False


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    import re
    
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip('. ')
    
    # Ensure filename is not empty
    if not sanitized:
        sanitized = "unnamed"
    
    return sanitized
