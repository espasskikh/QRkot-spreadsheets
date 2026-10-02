from fastapi import HTTPException, status


class TransactionError(HTTPException):

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Не удалось сохранить изменения в БД.'
        )


class YandexDiskError(HTTPException):
    """Ошибка при работе с API Яндекс Диска."""

    def __init__(
        self,
        detail: str,
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)
