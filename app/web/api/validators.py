from fastapi import HTTPException, status

from app.core.constants import ALLOWED_EXTENSIONS


def check_file_format(
    file_format: str,
) -> None:
    if file_format not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=406, detail="Only .jpg or .png  files allowed"
        )


def check_required_field(data: dict):
    missing_fields = [
        field for field, value in data.items() if value in [None, ""]
    ]
    if missing_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required form fields: {', '.join(missing_fields)}",
        )
