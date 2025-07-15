#!/usr/bin/env python3
"""
Enhanced Error Handler and Logging Utility
"""

import logging
import traceback
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Dict
from functools import wraps
import sys

class ErrorHandler:
    """Enhanced error handling and logging"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup error logger
        self.error_logger = self._setup_error_logger()
        self.error_count = 0
        self.max_errors = 100
        
    def _setup_error_logger(self):
        """Setup dedicated error logger"""
        error_logger = logging.getLogger('error_handler')
        error_logger.setLevel(logging.ERROR)
        
        # File handler for errors
        error_handler = logging.FileHandler(
            self.log_dir / 'errors.log',
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        
        # Error formatter
        error_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        error_handler.setFormatter(error_formatter)
        
        error_logger.addHandler(error_handler)
        return error_logger
    
    def log_error(self, error: Exception, context: Dict[str, Any] = None, 
                  severity: str = "ERROR"):
        """Log error with context information"""
        if self.error_count >= self.max_errors:
            return
            
        self.error_count += 1
        
        error_info = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {},
            'severity': severity,
            'python_version': sys.version,
            'working_directory': os.getcwd()
        }
        
        # Log to file
        self.error_logger.error(json.dumps(error_info, ensure_ascii=False, indent=2))
        
        # Also log to console for development
        if severity == "CRITICAL":
            print(f"🚨 CRITICAL ERROR: {error}")
        elif severity == "ERROR":
            print(f"❌ ERROR: {error}")
        elif severity == "WARNING":
            print(f"⚠️ WARNING: {error}")
    
    def handle_exception(self, func_name: str = "unknown"):
        """Decorator for handling exceptions in functions"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    self.log_error(e, {
                        'function': func_name,
                        'args': str(args)[:500],  # Limit args length
                        'kwargs': str(kwargs)[:500]
                    })
                    return None
            return wrapper
        return decorator
    
    def handle_async_exception(self, func_name: str = "unknown"):
        """Decorator for handling exceptions in async functions"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    self.log_error(e, {
                        'function': func_name,
                        'args': str(args)[:500],
                        'kwargs': str(kwargs)[:500]
                    })
                    return None
            return wrapper
        return decorator
    
    def create_error_report(self) -> str:
        """Create comprehensive error report"""
        error_log_file = self.log_dir / 'errors.log'
        
        if not error_log_file.exists():
            return "No errors logged"
        
        try:
            with open(error_log_file, 'r', encoding='utf-8') as f:
                error_logs = f.read()
            
            # Count different error types
            error_types = {}
            for line in error_logs.split('\n'):
                if '"error_type":' in line:
                    try:
                        error_data = json.loads(line.split(' - ', 3)[-1])
                        error_type = error_data.get('error_type', 'Unknown')
                        error_types[error_type] = error_types.get(error_type, 0) + 1
                    except:
                        continue
            
            report = f"""
# Error Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- Total Errors Logged: {self.error_count}
- Log File Size: {error_log_file.stat().st_size:,} bytes

## Error Types
"""
            for error_type, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True):
                report += f"- {error_type}: {count} occurrences\n"
            
            report += f"\n## Recent Errors (last 10)\n"
            recent_errors = error_logs.split('\n')[-20:]  # Last 20 lines
            for line in recent_errors[-10:]:
                if line.strip():
                    report += f"- {line}\n"
            
            return report
            
        except Exception as e:
            return f"Error generating report: {e}"

# Global error handler instance
error_handler = ErrorHandler()

# Convenience functions
def log_error(error: Exception, context: Dict[str, Any] = None, severity: str = "ERROR"):
    """Convenience function to log errors"""
    error_handler.log_error(error, context, severity)

def handle_exception(func_name: str = "unknown"):
    """Convenience decorator for exception handling"""
    return error_handler.handle_exception(func_name)

def handle_async_exception(func_name: str = "unknown"):
    """Convenience decorator for async exception handling"""
    return error_handler.handle_async_exception(func_name)

# Global exception handler
def setup_global_exception_handler():
    """Setup global exception handler for uncaught exceptions"""
    def global_exception_handler(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            # Allow Ctrl+C to work normally
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        error_handler.log_error(exc_value, {
            'global_exception': True,
            'traceback': ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        }, "CRITICAL")
        
        # Also print to stderr
        print(f"🚨 UNCAUGHT EXCEPTION: {exc_value}", file=sys.stderr)
    
    sys.excepthook = global_exception_handler

# Auto-setup global handler when imported
setup_global_exception_handler()