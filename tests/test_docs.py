import os
import re
import runpy
import sys
from glob import glob
from pathlib import Path

import pytest

from magicgui import type_map, use_app


@pytest.mark.parametrize(
    "fname",
    [
        f
        for f in glob("docs/**/*.md", recursive=True)
        if "_build" not in f and Path(f).read_text(encoding="utf-8").startswith("-")
    ],
)
def test_doc_code_cells(fname, globalns=globals()):
    """Make sure that all code cells in documentation perform as expected."""
    text = Path(fname).read_text()
    code_cells = re.findall(r"```{code-cell}[^\n]+\n(.*?)`{3}", text, re.S)
    for cell in code_cells:
        header = re.search(r"-{3}(.+?)-{3}", cell, re.S)
        if header:
            cell = cell.replace(header.group(), "")
            if "warns" in header.group():
                with pytest.warns(None):
                    exec(cell, globalns)
                continue
            if "raises-exception" in header.group():
                with pytest.raises(Exception):
                    exec(cell, globalns)
                continue
        exec(cell, globalns)


@pytest.mark.parametrize(
    "fname", [f for f in glob("examples/*.py") if "napari" not in f]
)
def test_examples(fname):
    """Make sure that all code cells in documentation perform as expected."""
    if "table.py" in fname and os.name == "nt" and sys.version_info < (3, 8):
        pytest.mark.skip()
        return
    app = use_app()
    app.start_timer(0, app.quit)
    try:
        runpy.run_path(fname)
    except ImportError as e:
        if "Numpy required to use images" in str(e):
            pytest.skip("numpy unavailable: skipping image example")
    finally:
        if "waveform" in fname:
            type_map._TYPE_DEFS.pop(int, None)
            type_map._TYPE_DEFS.pop(float, None)
