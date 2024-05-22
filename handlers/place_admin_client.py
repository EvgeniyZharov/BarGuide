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


class PAClient:
    btn_pa_main_menu = ["Мое заведение",
                        "Смотреть заведения",
                        "Найти заведение",
                        "Заведения рядом",
                        "Мероприятия",
                        "О проекте",
                        ]
    btn_settings = ["Список резервов",
                    "Настройки меню",
                    "Настройки информации о заведении",
                    ]

    def __init__(self, data_client: DataClient):
        self.data_client = data_client

        self.PlaceSettings = PlaceSettings(data_client=data_client)
        self.AnnounceSettings = AnnounceSettings(data_client=data_client)

    async def set_new_place_admin(self, msg: types.Message):
        places = self.data_client.get_place_list()
        await msg.answer("Выберите заведение, в котором Вы работаете.",
                         reply_markup=create_keyboards(places))
        await FSMWorkProgram.start_create_pa.set()

    async def save_new_pa(self, msg: types.Message):
        if self.data_client.place_exist(msg.text):
            place_id = self.data_client.get_place_id(msg.text)
            result = self.data_client.set_place_admin(user_id=msg.from_user.id,
                                                      user_name=msg.from_user.full_name,
                                                      place_id=place_id)
            if result:
                await msg.answer(f"Вы успешно зарегистрированы, как администратор {msg.text}.",
                                 reply_markup=create_keyboards(self.btn_pa_main_menu))
                await FSMWorkProgram.pa_main_menu.set()

            else:
                await msg.answer("Произошла ошибка. Сейчас зарегистрироваться нельзя")
        else:
            await msg.answer("Такого заведения нет, выберите из существующих.")

    def run_handler(self):
        dp.register_message_handler(self.set_new_place_admin,
                                    Text(equals="ww", ignore_case=True),
                                    state="*")
        dp.register_message_handler(self.save_new_pa,
                                    state=FSMWorkProgram.start_create_pa)

        # dp.register_message_handler(self.place_settings,
        #                             Text(equals="Мое заведение", ignore_case=True),
        #                             state=FSMWorkProgram.pa_main_menu)


        # Run function

