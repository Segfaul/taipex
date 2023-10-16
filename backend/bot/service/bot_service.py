import json
import inspect

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import aiogram.utils.markdown as md

from backend.config import logger, log


class Form_Product(StatesGroup):
    product_info = State()

class Form(StatesGroup):
    percent = State()


class TelegramBot:

    def __init__(self, api_token: str, api_service, web_app_url: str):
        self.bot = Bot(token=api_token)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())
        self.api_service = api_service
        self.web_app_url = web_app_url

        self.handlers()

    @classmethod
    def keyboard(cls, commands: list[list]) -> types.ReplyKeyboardMarkup:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        for row in commands:
            markup.row(
                *list(map(types.KeyboardButton, row))
            )

        return markup

    @classmethod
    def main_menu(cls, user: dict = None) -> list:
        menu = [
            ["🎁 Products"],
            [
                f"UPD KEY ({user['api_key'][-4::] if user and user['api_key'] else 'unset'}...)",
                f"💡 {'ON' if user and user['notification'] else 'OFF'}"
            ],
            ["👤 ACC", "📎 HELP"]
        ]
        return menu

    @classmethod
    @property
    def admin_panel(cls) -> list:
        menu = [
            [
                "➕ ADD PRODUCT",
                "➖ DELETE PRODUCT"
            ],
            [
                "✔ PROMOTE USER",
                "♻ UPD PRODUCT"
            ],
            ["⬅ MENU"]
        ]

        return menu

    def handlers(self):

        @log(logger)
        @self.dp.message_handler(commands=['start'])
        async def commands_start(message: types.Message):
            if (await self.api_service.add_user(message.from_user.id, message.from_user.username)) == 0:
                for admin in (await self.api_service.get_user_list_admin):
                    await self.bot.send_message(
                        admin['id'],
                        f"&#128314           "
                        f"{md.hitalic('New user')}           "
                        f"&#128314\n\nStats:\n"
                        f"├{md.hbold('ID')}: {md.hcode(message.from_user.id)}\n"
                        f"├{md.hbold('Nick')}: @{message.from_user.username}\n"
                        f"├{md.hbold('Is_bot')}: {message.from_user.is_bot}\n"
                        , parse_mode='html'
                    )

            user = await self.api_service.get_user(message.from_user.id)
            menu = self.main_menu(user)

            if user['is_admin']:
                menu.append(['➡ ADMIN_PANEL'])

            markup = TelegramBot.keyboard(menu)
            await self.bot.set_chat_menu_button(message.from_user.id, types.MenuButtonWebApp('web', web_app=types.WebAppInfo(url=self.web_app_url)))

            await self.bot.send_message(
                message.from_user.id,
                f"Welcome back, @{message.from_user.username if message.from_user.username else 'user'}\n",
                parse_mode='html',
                reply_markup=markup
            )

            await message.delete()

        #  --------------------User Logic--------------------

        @log(logger)
        @self.dp.message_handler(commands=['account', 'acc', 'акк', 'аккаунт'])
        @self.dp.message_handler(Text(equals=['👤 ACC'], ignore_case=True))
        async def commands_account(message: types.Message):
            user = await self.api_service.get_user(message.from_user.id)

            menu = self.main_menu(user)
            if user['is_admin']:
                menu.append(['➡ ADMIN_PANEL'])
            markup = TelegramBot.keyboard(menu)

            await self.bot.send_message(
                message.from_user.id,
                f"\n&#128100My Profile:\n"
                f"\n&#128273API_key: {md.hspoiler(user['api_key'])}"
                f"\n&#128276Alerts: {'on' if user['notification'] else 'off'}",
                parse_mode='html',
                reply_markup=markup
            )
            await message.delete()

        @log(logger)
        @self.dp.message_handler(commands=['help', 'hlp', 'hp', 'поддержка'])
        @self.dp.message_handler(Text(equals=['📎 HELP'], ignore_case=True))
        async def commands_help(message: types.Message):
            user = await self.api_service.get_user(message.from_user.id)
            menu = self.main_menu(user)
            if user['is_admin']:
                menu.append(['➡ ADMIN_PANEL'])
            markup = TelegramBot.keyboard(menu)

            await self.bot.send_message(
                message.from_user.id,
                f"&#128206Details on each of the commands&#128206\n\n"
                f"/acc {md.hitalic('- get your bot account details')}\n"
                f"/sw {md.hitalic('- to resume/break connection to market updates')}\n"
                f"/product {md.hitalic('- get up-to-date product list')}\n",
                parse_mode='html',
                reply_markup=markup
            )

            await message.delete()

        @log(logger)
        @self.dp.message_handler(commands=['status', 'st', 'switch', 'sw', 'change'])
        @self.dp.message_handler(Text(contains=['💡'], ignore_case=True))
        async def commands_status(message: types.Message):
            result = await self.api_service.update_notification(message.from_user.id)

            user = await self.api_service.get_user(message.from_user.id)
            menu = self.main_menu(user)
            if user['is_admin']:
                menu.append(['➡ ADMIN_PANEL'])
            markup = TelegramBot.keyboard(menu)

            if result == 1:
                await self.bot.send_message(
                    message.from_user.id,
                    f"Alerts {md.hbold('on')}...\n\n"
                    f"As soon as I find a good deal, I'll send a notification&#9203"
                    f"To disable notifications, type &#128073 /sw",
                    parse_mode='html',
                    reply_markup=markup
                )

            else:
                await self.bot.send_message(
                    message.from_user.id,
                    f"Alerts {md.hbold('off')}...\n\n"
                    f"To enable notifications, type &#128073 /sw",
                    parse_mode='html',
                    reply_markup=markup
                )

            await message.delete()

        @log(logger)
        @self.dp.message_handler(commands=['add_product', 'add_pr', 'new_pr'])
        @self.dp.message_handler(Text(contains=['➕'], ignore_case=True))
        async def commands_add_product(message: types.Message):
            markup = TelegramBot.keyboard(
                [
                    ['X']
                ]
            )

            await Form_Product.product_info.set()
            await self.bot.send_message(
                message.from_user.id,
                "Enter product info in the following form &#10549\n"
                "\n{\n"
                '   "title": "...",\n'
                '   "price": "...",\n'
                '   "description": "...",\n'
                '   "img_url": "https://..."\n'
                "}\n\n"
                "To cancel, type the command 👉 /cancel",
                parse_mode='html',
                reply_markup=markup
            )

            await message.delete()

        @log(logger)
        @self.dp.message_handler(commands=['upd_product', 'upd_pr'])
        @self.dp.message_handler(Text(contains=['♻'], ignore_case=True))
        async def commands_upd_product(message: types.Message):
            markup = TelegramBot.keyboard(
                [
                    ['X']
                ]
            )

            await Form_Product.product_info.set()
            await self.bot.send_message(
                message.from_user.id,
                "Enter product info in the following form &#10549\n"
                "\n{\n"
                '   "product_id": "...",\n'
                '   "title": "...",\n'
                '   "price": "...",\n'
                '   "description": "...",\n'
                '   "img_url": "https://..."\n'
                "}\n\n"
                "To cancel, type the command 👉 /cancel",
                parse_mode='html',
                reply_markup=markup
            )

            await message.delete()

        @log(logger)
        @self.dp.message_handler(commands=['del_product', 'del_pr'])
        @self.dp.message_handler(Text(contains=['➖'], ignore_case=True))
        async def commands_del_product(message: types.Message):
            markup = TelegramBot.keyboard(
                [
                    ['X']
                ]
            )

            await Form_Product.product_info.set()
            await self.bot.send_message(
                message.from_user.id,
                "Enter product info in the following form &#10549\n"
                "\n{\n"
                '   "product_id": "...",\n'
                "}\n\n"
                "To cancel, type the command 👉 /cancel",
                parse_mode='html',
                reply_markup=markup
            )

            await message.delete()

        @self.dp.message_handler(state='*', commands='cancel')
        @self.dp.message_handler(Text(equals=['cancel', 'отмена', '❌', 'X'], ignore_case=True), state='*')
        async def cancel_handler(message: types.Message, state: FSMContext):
            func_name = inspect.currentframe().f_code.co_name

            try:

                await message.delete()

                current_state = await state.get_state()
                if current_state is None:
                    return

                if current_state.split(':')[1] in ['some_state']:
                    # Base User state handler
                    user = await self.api_service.get_user(message.from_user.id)
                    menu = self.main_menu(user)
                    if user['is_admin']:
                        menu.append(['➡ ADMIN_PANEL'])
                    markup = TelegramBot.keyboard(menu)

                else:
                    markup = TelegramBot.keyboard(self.admin_panel)

                await self.bot.send_message(message.from_user.id, "Input stopped &#128219", parse_mode='html',
                                            reply_markup=markup)

                await self.bot.delete_message(
                    message.from_user.id, message.message_id - 1
                )

            except Exception as error:
                logger.error("%s/%s||%s", func_name, error.__class__, error.args[0])

            finally:
                await state.finish()
                logger.info("%s", func_name)

        @self.dp.message_handler(state=Form_Product.product_info)
        async def process_product_info(message: types.Message, state: FSMContext):
            func_name = inspect.currentframe().f_code.co_name

            try:
                async with state.proxy() as data:
                    data['product_info'] = message.text

                product_info = json.loads(data['product_info'])

                if 'product_id' in [*product_info]:
                    if len([*product_info]) == 1:
                        result = await self.api_service.delete_product(**product_info)
                    
                    else:
                        result = await self.api_service.update_product(**product_info)

                else:
                    result = await self.api_service.add_product(**product_info)

                replies = {201: 'added', 200: 'updated', 204: 'deleted'}

                if int(*result) in [*replies]:

                    await self.bot.send_message(
                        message.from_user.id,
                        md.text(
                            md.text(
                                f"Product {replies[int(*result)]} successfully &#10004"
                            ),
                            sep='\n',
                        ),
                        parse_mode='html',
                        reply_markup=TelegramBot.keyboard(self.admin_panel)
                    )

                else:
                    await self.bot.send_message(
                        message.from_user.id, "Incorrect input &#128219 \n"
                                              "Try again 👇", parse_mode='html',
                        reply_markup=TelegramBot.keyboard(self.admin_panel)
                    )

            except Exception as warning:
                print(warning)
                try:

                    await self.bot.send_message(
                        message.from_user.id, "Unexpected error &#128219 \n"
                                              "Try again 👇", parse_mode='html',
                        reply_markup=TelegramBot.keyboard(self.admin_panel)
                    )
                    logger.warning("%s/%s||%s", func_name, warning.__class__, warning.args[0])

                except Exception as error:
                    logger.error("%s/%s||%s", func_name, error.__class__, error.args[0])

            finally:
                await state.finish()
                logger.info("%s", func_name)

        #  --------------------Admin Logic--------------------

        @log(logger)
        @self.dp.message_handler(Text(equals=['⬅ MENU'], ignore_case=True))
        async def back_to_menu(message: types.Message):
            if message.from_user.id in [admin['id'] for admin in (await self.api_service.get_user_list_admin)]:
                user = await self.api_service.get_user(message.from_user.id)
                menu = self.main_menu(user)
                if user['is_admin']:
                    menu.append(['➡ ADMIN_PANEL'])
                markup = TelegramBot.keyboard(menu)

                await self.bot.send_message(
                    message.from_user.id,
                    f"Welcome back, @{message.from_user.username if message.from_user.username else 'user'}\n",
                    parse_mode='html',
                    reply_markup=markup
                )

                await message.delete()

        @log(logger)
        @self.dp.message_handler(Text(equals=['➡ ADMIN_PANEL'], ignore_case=True))
        async def enter_admin_panel(message: types.Message):
            if message.from_user.id in [admin['id'] for admin in (await self.api_service.get_user_list_admin)]:
                menu = self.admin_panel
                markup = TelegramBot.keyboard(menu)

                await self.bot.send_message(
                    message.from_user.id,
                    f"&#128272 Welcome to {md.hbold('TRACKER')} ADMIN PANEL, "
                    f"@{message.from_user.username if message.from_user.username else 'user'}\n",
                    parse_mode='html',
                    reply_markup=markup
                )

                await message.delete()

    def start(self, skip_updates: bool = True):
        executor.start_polling(self.dp, skip_updates=skip_updates)