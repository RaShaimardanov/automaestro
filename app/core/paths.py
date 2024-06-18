from pathlib import Path, PurePath
from typing import Final

# Path to the root of project
ROOT_DIR: Final[Path] = Path(__file__).parent.parent

BOT_FOLDER = PurePath(ROOT_DIR / "bot/")
WEB_APP_FOLDER = PurePath(ROOT_DIR / "web/")

TEMPLATES_FOLDER = PurePath(WEB_APP_FOLDER / "templates/")
STATIC_FOLDER = PurePath(TEMPLATES_FOLDER / "static/")

RESOURCES_DIR = PurePath(ROOT_DIR / "resources")
LOCALES_DIR = PurePath(RESOURCES_DIR / "locales/")
