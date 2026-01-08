from fastapi import HTTPException, status


class InvalidImageType(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Недопустимый тип файла. Разрешены: JPG, PNG, WEBP",
        )


class ImageTooLarge(HTTPException):
    def __init__(self, max_mb: int):
        super().__init__(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Файл слишком большой. Максимум {max_mb} MB",
        )


class InvalidImageContent(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Файл не является корректным изображением",
        )


class InvalidFileType(HTTPException):
    def __init__(self, allowed: str | None = None):
        detail = "Недопустимое расширение файла 3D-модели"
        if allowed:
            detail += f". Разрешены: {allowed}"

        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class InvalidMimeType(HTTPException):
    def __init__(self, allowed: str | None = None):
        detail = "Недопустимый MIME-тип файла 3D-модели"
        if allowed:
            detail += f". Разрешены: {allowed}"

        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class FileTooLarge(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Файл 3D-модели слишком большой. Максимум {10} MB",
        )
