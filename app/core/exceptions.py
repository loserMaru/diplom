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
