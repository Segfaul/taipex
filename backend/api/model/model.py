import secrets

from tortoise import fields
from tortoise.models import Model

from backend.api.validator.product_validator import NullOrPositive, LinkOrFake


class User(Model):
    """
    Telegram User Model
    """
    id = fields.BigIntField(pk=True)

    username = fields.CharField(max_length=32, null=True, default=None)
    is_admin = fields.BooleanField(default=False)
    notification = fields.BooleanField(default=False)
    api_key = fields.CharField(max_length=16, default=secrets.token_hex(8), unique=True)

    modified_date = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"


class Product(Model):
    """
    Product Model
    """
    id = fields.BigIntField(pk=True)

    title = fields.CharField(max_length=100)
    description = fields.TextField(null=True, default=None)
    img_url = fields.CharField(max_length=255, null=True, default=None, validators=[LinkOrFake()])

    price = fields.DecimalField(max_digits=10, decimal_places=2, validators=[NullOrPositive()])

    modified_date = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "products"
