from fastapi import APIRouter, HTTPException

from backend.api.service.user_service import UserService
from backend.api.service.product_service import ProductService


router = APIRouter(
    prefix='/product',
)

user_service = UserService()
product_service = ProductService()


@router.post("/create", tags=["Product"])
async def add_product(
        api_key: str, title: str, price: float,
        description: str = None, img_url: str = None
    ):
    """
    Add **product** in database
    """
    admin_objs = await user_service.get_admins
    
    if api_key in [admin_obj['api_key'] for admin_obj in admin_objs]:
        response = await product_service.add_product(title=title, price=price, description=description, img_url=img_url)

        if response == 0:
            return {201: "Succesfully added product"}

        raise HTTPException(status_code=404, detail="Something went wrong...")

    raise HTTPException(status_code=403, detail="Not enough rights to perform such an action")

@router.get("/get", tags=["Product"])
async def get_product(product_id: int):
    """
    Get specific **product** from database
    """
    response = await product_service.get_product(product_id=product_id)

    if response:
        return response

    raise HTTPException(status_code=404, detail="No such product found in database")


@router.get("/list", tags=["Product"])
async def get_products():
    """
    Get **product** list from database.
    """
    response = await product_service.get_products

    if response:
        return response

    raise HTTPException(status_code=404, detail="No products found in database")


@router.put("/update", tags=["Product"])
async def update_product(
        api_key: str, product_id: int, title: str, price: float,
        description: str = None, img_url: str = None
    ):
    """
    Update **product** instance. Restricted to *non-admin users*.
    """
    admin_objs = await user_service.get_admins
    
    if api_key in [admin_obj['api_key'] for admin_obj in admin_objs]:
        response = await product_service.update_product(product_id=product_id, title=title, price=price, description=description, img_url=img_url)

        if response != -1:
            return response
        
        raise HTTPException(status_code=404, detail="No product with such id found in database")

    raise HTTPException(status_code=403, detail="Not enough rights to perform such an action")


@router.delete("/delete", tags=["Product"])
async def delete_product(api_key: str, product_id: int):
    """
    Delete **product** instance. Restricted to *non-admin users*.
    """
    admin_objs = await user_service.get_admins
    
    if api_key in [admin_obj['api_key'] for admin_obj in admin_objs]:
        response = await product_service.delete_product(product_id)
        if response:
            return {204: "Succesfully deleted Product"}

        raise HTTPException(status_code=404, detail="No such product found in database")
    
    raise HTTPException(status_code=403, detail="Not enough rights to perform such an action")
