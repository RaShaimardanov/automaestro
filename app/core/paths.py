from pathlib import Path, PurePath
from typing import Final

# Path to the root of project
ROOT_DIR: Final[Path] = Path(__file__).parent.parent

BOT_FOLDER = PurePath(ROOT_DIR / "bot/")
WEB_APP_FOLDER = PurePath(ROOT_DIR / "web/")

TEMPLATES_FOLDER = PurePath(WEB_APP_FOLDER / "templates/")
STATIC_FOLDER = PurePath(TEMPLATES_FOLDER / "static/")

RESOURCES_DIR = PurePath(ROOT_DIR / "resources")
DATA_DIR = PurePath(RESOURCES_DIR / "data/")
VOICES_DIR = PurePath(DATA_DIR / "voices/")
IMAGES_DIR = PurePath(DATA_DIR / "images/")
QRCODES_DIR = PurePath(DATA_DIR / "qrcodes/")
LOCALES_DIR = PurePath(RESOURCES_DIR / "locales/")
