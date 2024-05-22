from aiogram import types
from initial import bot, dp
from keyboards import create_keyboards
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from dataClient.db_mysql import DataClient

from config import FSMWorkProgram


class ChoiceAnnounceProgram:
    def __init__(self, data_client: DataClient) -> None:
        self.data_client = data_client

    async def get_categories(self, msg: types.Message) -> None:
        categories_titles = self.data_client.get_announce_category()
        if categories_titles[0]:
            await msg.reply("Выберите, какого типа Вас интересуют мероприятия:",
                            reply_markup=create_keyboards(categories_titles[1], cancel_btn=True))
            await FSMWorkProgram.get_announce_category.set()
        else:
            await msg.reply("Скоро добавят новые категории мероприятий.")

    async def get_announce(self, msg: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            announce_category_id = self.data_client.get_announce_category_id(msg.text)
            data["announce_category"] = msg.text
            data["announce_category_id"] = announce_category_id
            announces = self.data_client.get_announce_from_category(announce_category_id)
            if announces[0]:
                await msg.reply("Выберите мероприятие:",
                                reply_markup=create_keyboards(announces[1], cancel_btn=True))
                await FSMWorkProgram.get_announce.set()

    async def choice_announce(self, msg: types.Message) -> None:
        announce_info = self.data_client.get_announce_info_for_title(msg.text)
        back_msg = f"{announce_info['title']}\n{announce_info['description']}\n\n" \
                   f"Ticker price: {announce_info['ticker_price']} руб.\nLink for paying: {announce_info['ticker_link']}"
        await msg.reply(back_msg)

    def run_handler(self) -> None:
        dp.register_message_handler(self.get_categories,
                                    Text(equals="Мероприятия", ignore_case=True),
                                    state=[FSMWorkProgram.main_menu,
                                           FSMWorkProgram.admin_main_menu,
                                           FSMWorkProgram.pa_main_menu])
        dp.register_message_handler(self.get_announce,
                                    state=FSMWorkProgram.get_announce_category)
        dp.register_message_handler(self.choice_announce,
                                    state=FSMWorkProgram.get_announce)


