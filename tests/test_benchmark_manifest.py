from caos.benchmark_manifest import ArtifactExpectation, BenchmarkManifest, verify_manifest


def test_manifest_checks_required_artifacts(tmp_path):
    (tmp_path / "README.md").write_text("run")
    manifest = BenchmarkManifest(
        artifacts=(ArtifactExpectation("README.md"), ArtifactExpectation("app.py")),
        verification_commands=(("python", "-c", "print('ok')"),),
    )
    report = verify_manifest(tmp_path, manifest)
    assert not report.artifacts_present
    assert report.missing_artifacts == ("app.py",)
    assert report.command_results[0].passed
    assert not report.passed


def test_manifest_passes_when_artifacts_and_commands_pass(tmp_path):
    (tmp_path / "README.md").write_text("run")
    (tmp_path / "app.py").write_text("print('ok')")
    manifest = BenchmarkManifest(
        artifacts=(ArtifactExpectation("README.md"), ArtifactExpectation("app.py")),
        verification_commands=(("python", "app.py"),),
    )
    report = verify_manifest(tmp_path, manifest)
    assert report.passed


def test_manifest_rejects_artifact_escape(tmp_path):
    manifest = BenchmarkManifest(
        artifacts=(ArtifactExpectation("../secret.txt"),), verification_commands=()
    )
    try:
        verify_manifest(tmp_path, manifest)
    except ValueError:
        pass
    else:
        raise AssertionError("artifact escape should be rejected")
