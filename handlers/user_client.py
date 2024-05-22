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
from handlers.user.choice_place import WatchPlacesProgram
from handlers.user.choice_announce import ChoiceAnnounceProgram
from handlers.user.find_place import FindPlaceProgram
from handlers.user.local_place import FindNearPlaceProgram
from handlers.user.choice_place_base import BaseChoicePlace

from handlers.admin_client import AdminClient
from handlers.place_admin_client import PAClient


class UserClient:
    btn_main_menu_for_user = ["Смотреть заведения",
                              "Найти заведение",
                              "Заведения рядом",
                              "Мероприятия",
                              "О проекте"]

    def __init__(self, data_client: DataClient) -> None:
        self.data_client = data_client
        self.WatchPlacesProgram = WatchPlacesProgram(data_client)
        self.ChoiceAnnounceProgram = ChoiceAnnounceProgram(data_client)
        self.FindNearPlaceProgram = FindNearPlaceProgram(data_client)
        self.FindPlaceProgram = FindPlaceProgram(data_client)
        # Base program for FindNear, FindPlace, WatchPlaces
        self.BaseChoicePlaceProgram = BaseChoicePlace(data_client)

        # Admin client
        self.AdminClient = AdminClient(data_client=data_client)

        # Place admin client
        self.PAClient = PAClient(data_client=data_client)

    def check_user_exist(self, msg: types.Message):
        user = msg.from_user
        if not self.data_client.user_exist(user.id):
            return self.data_client.set_user(name=user.full_name, tg_id=str(user.id))

    async def go_to_main_menu(self, msg: types.Message) -> None:
        result = self.check_user_exist(msg=msg)

        if self.data_client.user_is_admin(msg.from_user.id):
            await msg.reply("Привет, администратор!",
                            reply_markup=create_keyboards(self.AdminClient.btn_admin_main_menu))
            await FSMWorkProgram.admin_main_menu.set()
        elif self.data_client.user_is_pa(msg.from_user.id):
            await msg.reply("Привет, администратор заведения!",
                            reply_markup=create_keyboards(self.PAClient.btn_pa_main_menu))
            await FSMWorkProgram.pa_main_menu.set()
        else:
            await msg.reply("Вы попали в главное меню.",
                            reply_markup=create_keyboards(self.btn_main_menu_for_user))
            await FSMWorkProgram.main_menu.set()

    async def start_work(self, msg: types.Message) -> None:
        result = self.check_user_exist(msg=msg)
        if self.data_client.user_is_admin(msg.from_user.id):
            await msg.reply("Привет, администратор!",
                            reply_markup=create_keyboards(self.btn_main_menu_for_user))
            await FSMWorkProgram.admin_main_menu.set()
        elif self.data_client.user_is_pa(msg.from_user.id):
            await msg.reply("Привет, администратор заведения!",
                            reply_markup=create_keyboards(self.btn_main_menu_for_user))
            await FSMWorkProgram.pa_main_menu.set()
        else:
            await msg.reply("Привет!",
                            reply_markup=create_keyboards(self.btn_main_menu_for_user))
            await FSMWorkProgram.main_menu.set()

    async def about_us(self, msg: types.Message) -> None:
        result = self.check_user_exist(msg=msg)
        back_msg = "Проект: гид по барам"
        await msg.reply(back_msg)

    async def set_new_admin(self, msg: types.Message):
        result = self.data_client.set_new_admin(str(msg.from_user.id))
        if result:
            await msg.reply("Вам доступны функции администратора.",
                            reply_markup=create_keyboards(["Перейти"]))
            await FSMWorkProgram.to_admin_main_menu.set()
        else:
            await msg.reply("Вы уже админ.",
                            reply_markup=create_keyboards(["Перейти"]))
            await FSMWorkProgram.to_admin_main_menu.set()

    async def test_image(self, msg: types.Message):
        image_link = msg.photo[-1]["file_id"]
        await msg.answer(msg.photo[-1]["file_id"])
        await msg.answer_photo(image_link)

    def run_handler(self) -> None:
        dp.register_message_handler(self.start_work, commands=["start"], state="*")
        dp.register_message_handler(self.go_to_main_menu,
                                    Text(equals="Отмена", ignore_case=True),
                                    state="*")
        dp.register_message_handler(self.about_us,
                                    Text(equals="О проекте", ignore_case=True),
                                    state=FSMWorkProgram.main_menu)
        dp.register_message_handler(self.set_new_admin,
                                    Text(equals="to_admin", ignore_case=True),
                                    state="*")
        # dp.register_message_handler(self.test_image,
        #                             content_types=["photo"],
        #                             state="*"
        #                             )

        # Run programs for bot function
        self.WatchPlacesProgram.run_handler()
        self.FindNearPlaceProgram.run_handler()
        self.FindPlaceProgram.run_handler()
        self.ChoiceAnnounceProgram.run_handler()
        # Base program for FindNear, FindPlace, WatchPlaces
        self.BaseChoicePlaceProgram.run_handler()

        # Run function for admins
        self.AdminClient.run_handler()

        # Run function for place admins
        self.PAClient.run_handler()
