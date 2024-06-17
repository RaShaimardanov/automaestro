from pathlib import Path, PurePath
from typing import Final

# Path to the root of project
ROOT_DIR: Final[Path] = Path(__file__).parent.parent
WEB_APP_FOLDER = PurePath(ROOT_DIR / "web/")
BOT_FOLDER = PurePath(ROOT_DIR / "bot/")

TEMPLATES_FOLDER = PurePath(WEB_APP_FOLDER / "templates/")
STATIC_FOLDER = PurePath(TEMPLATES_FOLDER / "static/")
