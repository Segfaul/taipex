from backend.api.model.model import Product
from backend.config import logger, log


class ProductService:

    def __init__(self) -> None:
        ...

    #  --------------------User Logic--------------------
    @classmethod
    @log(logger)
    async def get_product(cls, product_id: int) -> dict or int:
        product_obj = await Product.filter(id=product_id).first().values()
        return product_obj
    
    @classmethod
    @property
    @log(logger)
    async def get_products(cls) -> list:
        product_objs = await Product.all().values()
        return product_objs

    #  --------------------Admin Logic--------------------
    @classmethod
    @log(logger)
    async def add_product(cls, title: str, price: float, description: str = None, img_url: str = None):
        await Product.create(title=title, price=price, description=description, img_url=img_url)
        return 0

    @classmethod
    @log(logger)
    async def delete_product(cls, product_id: int):
        product_obj = await Product.filter(id=product_id).first()

        if product_obj:
            await product_obj.delete()
            return 1
        
        return 0
    
    @classmethod
    @log(logger)
    async def update_product(cls, product_id: int, title: str, price: float, description: str = None, img_url: str = None):
        product_obj = await Product.filter(id=product_id).first()

        if product_obj:
            await product_obj.update_from_dict({"title": title, "price": price, "description": description, "img_url": img_url})
            await product_obj.save()
            return product_obj
