import sys
from pathlib import Path

from factory_tools.utils import get_file_path_depth

_FOLDER_LEVER: int = 3

_CURRENT_FOLDER = Path(__file__)

_FOLDER_NAME = get_file_path_depth(_CURRENT_FOLDER, _FOLDER_LEVER)

THIS_DIR = (
    Path(sys.executable).parent / "/".join(_FOLDER_NAME)
    if getattr(sys, "frozen", False)
    else _CURRENT_FOLDER.parent
)
