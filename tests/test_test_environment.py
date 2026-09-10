"""Exercise test isolation against a pre-existing shared temporary directory."""
import getpass
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('outcome', ['pass', 'fail'])
@pytest.mark.parametrize('from_tests_directory', [False, True])
def test_default_test_run_avoids_shared_root_and_cleans_up(tmp_path, outcome,
                                                        from_tests_directory):
    project = tmp_path / 'project'
    project.mkdir()
    (project / 'conftest.py').write_bytes((ROOT / 'conftest.py').read_bytes())
    (project / 'pytest.ini').write_bytes((ROOT / 'pytest.ini').read_bytes())
    test_dir = project / 'tests'
    test_dir.mkdir()
    shared = tmp_path / 'shared'
    shared.mkdir()
    predictable = shared / ('pytest-of-' + getpass.getuser())
    outside = tmp_path / 'outside'
    outside.mkdir()
    sentinel = outside / 'keep.txt'
    sentinel.write_text('Synthetic external sentinel.', encoding='utf-8')
    if os.name == 'posix':
        predictable.symlink_to(outside, target_is_directory=True)
    else:
        predictable.mkdir()
    result_path = tmp_path / 'result.json'
    (test_dir / 'test_probe.py').write_text(
        'import json, os\nfrom pathlib import Path\n'
        'def test_probe(tmp_path, tmp_path_factory):\n'
        '    base = tmp_path_factory.getbasetemp()\n'
        '    Path(os.environ["AWA_TEST_RESULT"]).write_text(json.dumps({\n'
        '        "base": str(base), "mode": base.parent.stat().st_mode & 0o777\n'
        '    }), encoding="utf-8")\n'
        '    (tmp_path / "output.txt").write_text("Synthetic output.", encoding="utf-8")\n'
        f'    assert {outcome == "pass"!r}\n', encoding='utf-8')
    env = dict(os.environ, TMPDIR=str(shared), TEMP=str(shared), TMP=str(shared),
               PYTEST_DEBUG_TEMPROOT=str(shared), PYTEST_ADDOPTS='',
               PYTEST_DISABLE_PLUGIN_AUTOLOAD='1', AWA_TEST_RESULT=str(result_path))
    result = subprocess.run([sys.executable, '-B', '-m', 'pytest', '-q',
                             '-p', 'no:cacheprovider'],
                            cwd=test_dir if from_tests_directory else project,
                            env=env, capture_output=True, timeout=30)
    assert result.returncode == (0 if outcome == 'pass' else 1), result.stderr
    recorded = json.loads(result_path.read_text(encoding='utf-8'))
    base = Path(recorded['base'])
    assert not base.is_relative_to(predictable)
    assert not base.is_relative_to(outside)
    assert not base.parent.exists(), 'The private test root should be cleaned after either outcome.'
    assert sentinel.read_text(encoding='utf-8') == 'Synthetic external sentinel.'
    assert list(outside.iterdir()) == [sentinel]
    if os.name == 'posix':
        assert recorded['mode'] == 0o700
