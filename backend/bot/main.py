import os
import asyncio
import inspect

from dotenv import load_dotenv

from backend.config import logger
from backend.bot.service.api_service import ApiService
from backend.bot.service.bot_service import TelegramBot


env = os.environ.get
load_dotenv('./.env')

API_TOKEN = env('API_TOKEN')
SERVICE_TOKEN = env('SERVICE_TOKEN')
API_URL = env('API_URL')
WEB_APP_URL = env('WEB_APP_URL')


async def main() -> None:
    func_name = inspect.currentframe().f_code.co_name

    try:

        api_service = ApiService(API_URL, SERVICE_TOKEN)

        aio_bot = TelegramBot(API_TOKEN, api_service, WEB_APP_URL)

        await aio_bot.dp.skip_updates()
        await aio_bot.dp.start_polling()

    except Exception as error:
        logger.error("%s/%s||%s", func_name, error.__class__, error.args[0])

    finally:
        session = await aio_bot.bot.get_session()
        await session.close()
        logger.info("%s", func_name)


if __name__ == '__main__':
    asyncio.run(main())
