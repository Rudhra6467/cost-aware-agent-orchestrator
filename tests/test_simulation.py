import pytest

from caos.simulation import ExecutionSimulator, SimTask


def test_simulator_finds_critical_path_and_parallelizes_independent_tasks():
    tasks = (
        SimTask("a", 10),
        SimTask("b", 20),
        SimTask("c", 5, ("a",)),
        SimTask("d", 7, ("b",)),
        SimTask("e", 3, ("c", "d")),
    )
    result = ExecutionSimulator().simulate(tasks)
    assert result.elapsed_minutes == 30
    assert result.critical_path == ("b", "d", "e")


def test_simulator_rejects_cycles():
    with pytest.raises(ValueError, match="cycle"):
        ExecutionSimulator().simulate((SimTask("a", 1, ("b",)), SimTask("b", 1, ("a",))))
