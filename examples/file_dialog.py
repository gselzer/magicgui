"""FileDialog with magicgui."""
from pathlib import Path
from typing import Sequence

from magicgui import magicgui, use_app


@magicgui(filename={"mode": "r"})
def filepicker(filename=Path("~")):
    """Take a filename and do something with it."""
    print("The filename is:", filename)
    return filename


# Sequence of paths
# We change the label using "label" for added clarity
# the filter argument restricts file types
@magicgui(filenames={"label": "Choose Tiff files:", "filter": "*.tif"})
def filespicker(filenames: Sequence[Path]):
    """Take a filename and do something with it."""
    print("The filenames are:", filenames)
    return filenames


filepicker.show()
filespicker.show()
filepicker.filename.changed.connect(print)
filespicker.filenames.changed.connect(print)

use_app().run()
