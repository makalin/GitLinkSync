import logging
import traceback
import sys
from typing import Callable, Any
from functools import wraps

class ErrorHandler:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.error_counts = {}
        self.recovery_strategies = {}

    def handle_error(self, error: Exception, context: str = "", retry_count: int = 0):
        """Handle an error with logging and recovery strategies."""
        error_type = type(error).__name__
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        
        # Log the error
        self.logger.error(f"Error in {context}: {error}")
        self.logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Try recovery strategy if available
        if error_type in self.recovery_strategies:
            try:
                return self.recovery_strategies[error_type](error, context, retry_count)
            except Exception as recovery_error:
                self.logger.error(f"Recovery strategy failed: {recovery_error}")
        
        return None

    def add_recovery_strategy(self, error_type: str, strategy: Callable):
        """Add a recovery strategy for a specific error type."""
        self.recovery_strategies[error_type] = strategy

    def get_error_summary(self) -> dict:
        """Get a summary of all errors encountered."""
        return {
            'total_errors': sum(self.error_counts.values()),
            'error_counts': dict(self.error_counts),
            'most_common_error': max(self.error_counts.items(), key=lambda x: x[1])[0] if self.error_counts else None
        }

    def reset_error_counts(self):
        """Reset error counts."""
        self.error_counts.clear()

def safe_execute(func: Callable, *args, **kwargs) -> Any:
    """Safely execute a function with error handling."""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        error_handler = ErrorHandler()
        return error_handler.handle_error(e, f"Function {func.__name__}")

def retry_on_error(max_retries: int = 3, delay: float = 1.0):
    """Decorator to retry a function on error."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_retries:
                        import time
                        time.sleep(delay * (2 ** attempt))  # Exponential backoff
                    else:
                        break
            raise last_error
        return wrapper
    return decorator

def log_errors(logger=None):
    """Decorator to log errors without stopping execution."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if logger:
                    logger.error(f"Error in {func.__name__}: {e}")
                    logger.error(traceback.format_exc())
                else:
                    print(f"Error in {func.__name__}: {e}")
                return None
        return wrapper
    return decorator
