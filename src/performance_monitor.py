import time
import psutil
import threading
from collections import defaultdict
from typing import Dict, List

class PerformanceMonitor:
    def __init__(self):
        self.metrics = defaultdict(list)
        self.start_times = {}
        self.api_calls = defaultdict(int)
        self.errors = defaultdict(int)
        self.lock = threading.Lock()

    def start_timer(self, operation: str):
        """Start timing an operation."""
        self.start_times[operation] = time.time()

    def end_timer(self, operation: str):
        """End timing an operation and record the duration."""
        if operation in self.start_times:
            duration = time.time() - self.start_times[operation]
            with self.lock:
                self.metrics[operation].append(duration)
            del self.start_times[operation]

    def record_api_call(self, api_name: str, success: bool = True):
        """Record an API call."""
        with self.lock:
            self.api_calls[api_name] += 1
            if not success:
                self.errors[api_name] += 1

    def get_memory_usage(self) -> Dict:
        """Get current memory usage."""
        process = psutil.Process()
        memory_info = process.memory_info()
        return {
            'rss': memory_info.rss,  # Resident Set Size
            'vms': memory_info.vms,  # Virtual Memory Size
            'percent': process.memory_percent()
        }

    def get_cpu_usage(self) -> float:
        """Get current CPU usage."""
        return psutil.cpu_percent()

    def get_operation_stats(self, operation: str) -> Dict:
        """Get statistics for a specific operation."""
        if operation not in self.metrics:
            return {}
        
        durations = self.metrics[operation]
        return {
            'count': len(durations),
            'avg_duration': sum(durations) / len(durations),
            'min_duration': min(durations),
            'max_duration': max(durations),
            'total_duration': sum(durations)
        }

    def get_api_stats(self) -> Dict:
        """Get API call statistics."""
        return {
            'total_calls': sum(self.api_calls.values()),
            'calls_by_api': dict(self.api_calls),
            'errors_by_api': dict(self.errors),
            'success_rate': {
                api: (self.api_calls[api] - self.errors[api]) / self.api_calls[api] * 100
                for api in self.api_calls
                if self.api_calls[api] > 0
            }
        }

    def get_system_stats(self) -> Dict:
        """Get system performance statistics."""
        return {
            'memory': self.get_memory_usage(),
            'cpu': self.get_cpu_usage(),
            'disk_usage': psutil.disk_usage('/').percent
        }

    def generate_report(self) -> Dict:
        """Generate a comprehensive performance report."""
        return {
            'system': self.get_system_stats(),
            'api_stats': self.get_api_stats(),
            'operations': {
                op: self.get_operation_stats(op)
                for op in self.metrics
            }
        }

    def reset(self):
        """Reset all metrics."""
        with self.lock:
            self.metrics.clear()
            self.api_calls.clear()
            self.errors.clear()
            self.start_times.clear()
