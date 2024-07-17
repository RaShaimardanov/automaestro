from qrcode.main import QRCode
from qrcode.constants import (
    ERROR_CORRECT_H,
)
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.moduledrawers import CircleModuleDrawer

from app.core.logger import logger
from app.core.config import settings
from app.core.paths import QRCODES_DIR


async def generate_qrcode(parameter: int):
    """Генерация QR-кода на основе параметра - telegram_id."""
    try:
        deep_link = f"tg://resolve?domain={settings.TELEGRAM.BOT_USERNAME}&start={parameter}"

        qr: QRCode = QRCode(version=2, error_correction=ERROR_CORRECT_H)

        qr.add_data(f"{deep_link}")
        qr.make(fit=True)

        image = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=CircleModuleDrawer(),
            color_mask=SolidFillColorMask(front_color=(18, 73, 127)),
            embeded_image_path=f"{QRCODES_DIR}/logo.jpg",
        )
        filename = f"{parameter}.jpg"
        image.save(QRCODES_DIR / filename)
        return filename

    except Exception as e:
        logger.error(f"Error generate qrcode: {parameter} - {str(e)}")
