class BaseServiceError(Exception):
    code = 500


class ItemNotFound(BaseServiceError):
    code = 404


class WrongPassword(BaseServiceError):
    code = 400
