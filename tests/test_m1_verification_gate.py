"""High-level invariants for the M1 verification boundary."""


def test_m1_gate_is_explicit():
    """The project must distinguish implementation completion from CI verification."""
    from pathlib import Path

    gate = Path(__file__).resolve().parents[1] / "docs" / "68-M1-VERIFICATION-GATE.md"
    assert gate.exists()
    text = gate.read_text(encoding="utf-8")
    assert "pytest -q" in text
    assert "zero failures" in text
    assert "idea -> understanding -> blueprint" in text
