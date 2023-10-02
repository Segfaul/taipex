from fastapi import APIRouter, HTTPException

from backend.api.service.user_service import UserService


router = APIRouter(
    prefix='/user',
)

user_service = UserService()


@router.post("/create", tags=["User"])
async def add_user(tg_id: int, username: str = None, is_admin: bool = False):
    """
    Add **user** in database
    """
    response = await user_service.add_user(tg_id=tg_id, username=username, is_admin=is_admin)

    if response == 0:
        return {201: "Succesfully added user"}

    raise HTTPException(status_code=404, detail="Something went wrong...")


@router.get("/get", tags=["User"])
async def get_user(tg_id: int):
    """
    Get specific **user** from database
    """
    response = await user_service.get_user(tg_id=tg_id)

    if response:
        return response

    raise HTTPException(status_code=404, detail="No such user found in database")


@router.get("/list", tags=["User"])
async def get_users(api_key: str):
    """
    Get **user** list from database. Restricted to non-admin users.
    """
    admin_objs = await user_service.get_admins
    
    if api_key in [admin_obj['api_key'] for admin_obj in admin_objs]:
        response = await user_service.get_users

        if response:
            return response

        raise HTTPException(status_code=404, detail="No users found in database")
    
    raise HTTPException(status_code=403, detail="Not enough rights to perform such an action")


@router.get("/list/admin", tags=["User"])
async def get_admin_users(api_key: str):
    """
    Get admin **user** list from database. Restricted to non-admin users.
    """
    admin_objs = await user_service.get_admins
    
    if api_key in [admin_obj['api_key'] for admin_obj in admin_objs]:
        response = await user_service.get_admins

        if response:
            return response

        raise HTTPException(status_code=404, detail="No users found in database")
    
    raise HTTPException(status_code=403, detail="Not enough rights to perform such an action")


@router.get("/list/upstream", tags=["User"])
async def get_ready_users(api_key: str):
    """
    Get ready **user** list from database. Restricted to *non-admin users*.
    """
    admin_objs = await user_service.get_admins
    
    if api_key in [admin_obj['api_key'] for admin_obj in admin_objs]:
        response = await user_service.get_ready_users

        if response:
            return response

        raise HTTPException(status_code=404, detail="No ready users found in database")
    
    raise HTTPException(status_code=403, detail="Not enough rights to perform such an action")


@router.put("/notification/change", tags=["User"])
async def update_notification(tg_id: int):
    """
    Change **user**'s notifications from 0 to 1 and reversed.
    """
    response = await user_service.update_notification(tg_id=tg_id)

    if response:
        return response
    
    raise HTTPException(status_code=404, detail="Rate Inusrance not found")


@router.put("/promote", tags=["User"])
async def promote_to_admin(api_key: str, tg_id: int, is_admin: int):
    """
    Promote **user** to an admin. Restricted to *non-admin users*.
    """
    admin_objs = await user_service.get_admins
    
    if api_key in [admin_obj['api_key'] for admin_obj in admin_objs]:
        response = await user_service.update_admin(tg_id=tg_id, status=is_admin)

        if response:
            return response
        
        raise HTTPException(status_code=404, detail="No user with such id found in database")

    raise HTTPException(status_code=403, detail="Not enough rights to perform such an action")
