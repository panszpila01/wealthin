"""
File Utilities for App

Common file processing utilities and validation functions.
"""

import streamlit as st
import pandas as pd
from typing import List


class FileUtils:
    """Utility class for file operations."""
    
    @staticmethod
    def validate_file_type(filename: str, supported_types: List[str]) -> bool:
        """Validate if the file type is supported."""
        if not filename:
            return False
        
        file_extension = filename.split('.')[-1].lower()
        return file_extension in [ext.lower() for ext in supported_types]
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human readable format."""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"


# Convenience functions for backward compatibility
def validate_file_type(filename: str, supported_types: List[str]) -> bool:
    """Validate if the file type is supported."""
    return FileUtils.validate_file_type(filename, supported_types)

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    return FileUtils.format_file_size(size_bytes)
