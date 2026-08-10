"""
TERATAI Exceptions
"""

class TerataiException(Exception):
    """Base Exception"""
    pass


class SheetNotFound(TerataiException):
    pass


class InvalidHeader(TerataiException):
    pass


class InvalidData(TerataiException):
    pass