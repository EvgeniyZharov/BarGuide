from aiogram import types
from initial import bot, dp
from keyboards import create_keyboards
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from config import FSMWorkProgram
from dataClient.db_mysql import DataClient
# from handlers.user.choice_place_base import ChoicePlaceBase


class WatchPlacesProgram:
    def __init__(self, data_client: DataClient) -> None:
        self.data_client = data_client
        # self.BaseChoicePlace = ChoicePlaceBase(data_client=data_client)

    async def get_categories(self, msg: types.Message) -> None:
        categories_titles = self.data_client.get_place_category()
        if categories_titles[0]:
            await msg.reply("Выберите, какого типа Вас интересует заведение:",
                            reply_markup=create_keyboards(categories_titles[1], cancel_btn=True))
            await FSMWorkProgram.get_place_category.set()
        else:
            await msg.reply("Скоро добавят новые категории заведений.")

    async def get_places(self, msg: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            place_category_id = self.data_client.get_place_category_id(msg.text)
            print(place_category_id)
            data["place_category"] = msg.text
            data["place_category_id"] = place_category_id
            places = self.data_client.get_place_from_category(place_category_id)
            if places[0]:
                await msg.reply("Выберите заведение:",
                                reply_markup=create_keyboards(places[1], cancel_btn=True))
                await FSMWorkProgram.get_place.set()
            else:
                await msg.reply("Скоро добавят новые заведения.")

    def run_handler(self) -> None:
        dp.register_message_handler(self.get_categories,
                                    Text(equals="Смотреть заведения", ignore_case=True),
                                    state=[FSMWorkProgram.main_menu,
                                           FSMWorkProgram.admin_main_menu,
                                           FSMWorkProgram.pa_main_menu])
        dp.register_message_handler(self.get_places,
                                    state=FSMWorkProgram.get_place_category)

