"""Frozen workloads used for reproducible CAOS experiments."""

from .benchmark_runner import BenchmarkTask


BENCHMARK_001_TODO_API = [
    BenchmarkTask("todo-1", "Create a todo through the REST API."),
    BenchmarkTask("todo-2", "List todos through the REST API."),
    BenchmarkTask("todo-3", "Mark a todo complete through the REST API."),
    BenchmarkTask("todo-4", "Delete a todo through the REST API."),
    BenchmarkTask("todo-5", "Persist todo data across process restart."),
    BenchmarkTask("todo-6", "Reject malformed todo input with a controlled response."),
    BenchmarkTask("todo-7", "Provide automated tests covering the required operations."),
    BenchmarkTask("todo-8", "Provide README instructions for running and testing the project."),
]
