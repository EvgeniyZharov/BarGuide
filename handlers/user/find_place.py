from aiogram import types
from initial import bot, dp
from keyboards import create_keyboards
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from dataClient.db_mysql import DataClient

# from handlers.user.choice_place import
from config import FSMWorkProgram
# from handlers.user.choice_place_base import ChoicePlaceBase


class FindPlaceProgram:
    def __init__(self, data_client: DataClient) -> None:
        self.data_client = data_client
        # self.WatchPlacesProgram = ChoicePlaceBase(data_client)

    @staticmethod
    async def set_title_place(msg: types.Message) -> None:
        await msg.answer("Введите название заведения, которое Вас интересует.",
                         reply_markup=create_keyboards(list(), cancel_btn=True))
        await FSMWorkProgram.set_title_place.set()

    async def get_suitable_place(self, msg: types.Message) -> None:
        places = self.data_client.get_suitable_place(msg.text)
        if places[0]:
            await msg.reply("Вот наиболее подходящие варианты.",
                            reply_markup=create_keyboards(places[1], cancel_btn=True))
            await FSMWorkProgram.get_place.set()
        else:
            await msg.reply("К сожалению, ничего не найдено. Попробуйте другой запрос")

    def run_handler(self) -> None:
        dp.register_message_handler(self.set_title_place,
                                    Text(equals="Найти заведение", ignore_case=True),
                                    state=[FSMWorkProgram.main_menu,
                                           FSMWorkProgram.admin_main_menu,
                                           FSMWorkProgram.pa_main_menu])
        dp.register_message_handler(self.get_suitable_place,
                                    state=FSMWorkProgram.set_title_place)


