import aiohttp

from backend.config import logger, log


class ApiService:

    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url
        self.api_key = api_key

    @log(logger)
    async def call_api(self, root: str, method: str = "GET", params: dict = None):
        link = self.base_url + root
        async with aiohttp.ClientSession() as session:
            if method == "GET":
                async with session.get(link, params=params) as response:
                    content = await response.json()
                    return content
            elif method == "POST":
                async with session.post(link, params=params) as response:
                    content = await response.json()
                    return content
            elif method == "PUT":
                async with session.put(link, params=params) as response:
                    content = await response.json()
                    return content
            elif method == "DELETE":
                async with session.delete(link) as response:
                    content = await response.json()
                    return content
            else:
                raise ValueError("Unsupported HTTP method")

    #  --------------------User Api--------------------

    @log(logger)
    async def add_user(self, tg_id: int, username: str = None, is_admin: bool = False):
        response = await self.call_api(
            root='/user/create',
            method='POST',
            params={'tg_id': tg_id, 'username': username, 'is_admin': str(is_admin)}
        )
        return response

    @log(logger)
    async def get_user(self, tg_id: int):
        response = await self.call_api(
            root='/user/get',
            method='GET',
            params={'tg_id': tg_id}
        )
        return response

    @log(logger)
    async def get_user_list(self):
        response = await self.call_api(
            root='/user/list',
            method='GET',
            params={'api_key': self.api_key}
        )
        return response

    @log(logger)
    async def get_user_list_upstream(self):
        response = await self.call_api(
            root='/user/list/upstream',
            method='GET',
            params={'api_key': self.api_key}
        )
        return response

    @log(logger)
    async def change_notification(self, tg_id: int):
        response = await self.call_api(
            root='/user/notification/change',
            method='PUT',
            params={'tg_id': tg_id, 'api_key': self.api_key}
        )
        return response

    @log(logger)
    async def change_admin(self, tg_id: int, is_admin: int):
        response = await self.call_api(
            root='/user/promote',
            method='PUT',
            params={'tg_id': tg_id, 'api_key': self.api_key, 'is_admin': is_admin}
        )
        return response

    #  --------------------Product Api--------------------

    @log(logger)
    async def add_product(
        self,
        title: str, price: float, description: str = None, img_url: str = None
    ):
        response = await self.call_api(
            root='/product/create',
            method='POST',
            params={
                'title': title, 'price': price, 'description': description, 'img_url': img_url, 
                'api_key': self.api_key
            }
        )
        return response

    @log(logger)
    async def get_product(self, product_id: int):
        response = await self.call_api(
            root='/product/get',
            method='GET',
            params={'product_id': product_id}
        )
        return response

    @log(logger)
    async def get_product_list(self):
        response = await self.call_api(
            root='/product/list',
            method='GET',
            params={}
        )
        return response

    @log(logger)
    async def update_product(
        self,
        product_id: int, title: str, price: float,
        description: str = None, img_url: str = None
    ):
        response = await self.call_api(
            root='/product/update',
            method='PUT',
            params={
                'product_id': product_id, 
                'title': title, 'price': price, 'description': description, 'img_url': img_url, 
                'api_key': self.api_key
            }
        )
        return response

    @log(logger)
    async def delete_product(self, product_id: int):
        response = await self.call_api(
            root='/product/delete',
            method='DELETE',
            params={'product_id': product_id, 'api_key': self.api_key}
        )
        return response
