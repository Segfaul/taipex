from tortoise.exceptions import ValidationError
from tortoise.validators import Validator


class NullOrPositive(Validator):
    """
    Validator made to check if value is >=0 or Null
    """
    def __call__(self, value: int):
        if value < 0:
            raise ValidationError("Provided value should be positive")


class LinkOrFake(Validator):
    """
    Validator made to check if provided link is valid / not
    """
    def __call__(self, value: str):
        if value[:5] != 'https':
            raise ValidationError("Provided value should be URL (*https://example.com/)")
