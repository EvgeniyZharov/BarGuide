from aiogram import types
from initial import bot, dp
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from dataClient.db_mysql import DataClient

from keyboards import create_keyboards
from config import FSMWorkProgram

from handlers.admin.PlaceSettings import PlaceSettings
from handlers.admin.AnnounceSettings import AnnounceSettings


class AdminClient:
    btn_admin_main_menu = ["Смотреть заведения",
                           "Найти заведение",
                           "Заведения рядом",
                           "Мероприятия",
                           "О проекте",
                           "Системные настройки"]
    btn_settings = ["Настройки: заведения",
                    "Настройки: мероприятия"]

    def __init__(self, data_client: DataClient):
        self.data_client = data_client

        #
        self.PlaceSettings = PlaceSettings(data_client=data_client)
        self.AnnounceSettings = AnnounceSettings(data_client=data_client)

    async def start_admin_main_menu(self, msg: types.Message):
        await msg.answer("Привет,администратор!",
                         reply_markup=create_keyboards(self.btn_admin_main_menu))
        await FSMWorkProgram.admin_main_menu.set()

    async def settings(self, msg: types.Message):
        await msg.answer("Выберите, какой режим планируете настроить.",
                         reply_markup=create_keyboards(self.btn_settings))
        await FSMWorkProgram.admin_settings.set()

    def run_handler(self):
        dp.register_message_handler(self.start_admin_main_menu,
                                    Text(equals="Перейти", ignore_case=True),
                                    state=FSMWorkProgram.to_admin_main_menu)
        dp.register_message_handler(self.settings,
                                    Text(equals="Системные настройки", ignore_case=True),
                                    state=FSMWorkProgram.admin_main_menu)

        # Run function
        self.PlaceSettings.run_handler()
        self.AnnounceSettings.run_handler()

