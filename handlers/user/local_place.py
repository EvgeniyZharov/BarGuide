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
# from handlers.user.choice_place import WatchPlacesProgram


class FindNearPlaceProgram:
    def __init__(self, data_client: DataClient) -> None:
        self.data_client = data_client
        # self.WatchPlacesProgram = WatchPlacesProgram(data_client)

    @staticmethod
    async def set_self_location(msg: types.Message) -> None:
        self_location_btn = ReplyKeyboardMarkup(resize_keyboard=True)
        self_location_btn.add(KeyboardButton("Поделиться местоположением", request_location=True))
        self_location_btn.add(KeyboardButton("Отмена"))
        await msg.answer("Отправьте свое местоположение, тогда мы найдем ближайшие к Вам заведения.",
                         reply_markup=self_location_btn)
        await FSMWorkProgram.set_self_location.set()

    async def get_near_place(self, msg: types.Message) -> None:
        user_lat = msg.location.latitude
        user_long = msg.location.longitude
        places_titles = self.data_client.get_near_position_place(f"{user_lat}_{user_long}",
                                                                 radius=5.0)
        if places_titles[0]:
            await msg.reply("Наиболее ближайшие к Вам заведения.",
                            reply_markup=create_keyboards(places_titles[1], cancel_btn=True))
            await FSMWorkProgram.get_place.set()
        else:
            await msg.reply("Рядом с вами ничего не обнаружено.",
                            reply_markup=create_keyboards(list(), cancel_btn=True))

    def run_handler(self) -> None:
        dp.register_message_handler(self.set_self_location,
                                    Text(equals="Заведения рядом", ignore_case=True),
                                    state=[FSMWorkProgram.main_menu,
                                           FSMWorkProgram.admin_main_menu,
                                           FSMWorkProgram.pa_main_menu])
        dp.register_message_handler(self.get_near_place,
                                    content_types=["location"],
                                    state=FSMWorkProgram.set_self_location)
