"""Give each test run its own private temporary root, including on Python 3.9."""
from pathlib import Path
import tempfile

import pytest


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # pytest 8 is the final series for Python 3.9. Avoid its predictable shared
    # temporary root (CVE-2025-71176); mkdtemp creates a fresh owner-only parent.
    # An explicit --basetemp remains the test runner's own choice.
    if config.option.basetemp is None:
        temporary = tempfile.TemporaryDirectory(prefix='awa-tests-')
        config.add_cleanup(temporary.cleanup)
        config.option.basetemp = str(Path(temporary.name) / 'work')
