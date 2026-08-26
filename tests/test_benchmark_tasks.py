from caos.benchmark_tasks import BENCHMARK_001_TODO_API


def test_benchmark_001_is_frozen_and_complete():
    assert len(BENCHMARK_001_TODO_API) == 8
    assert [task.task_id for task in BENCHMARK_001_TODO_API] == [
        "todo-1", "todo-2", "todo-3", "todo-4", "todo-5", "todo-6", "todo-7", "todo-8"
    ]
