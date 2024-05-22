from aiogram import types
from initial import bot, dp
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from dataClient.db_mysql import DataClient

from keyboards import create_keyboards
from config import FSMWorkProgram


class AnnounceSettings:
    btn_admin_main_menu = ["Смотреть заведения",
                           "Найти заведение",
                           "Заведения рядом",
                           "Мероприятия",
                           "О проекте",
                           "Системные настройки"]
    btn_announce_settings = ["Добавить категорию",
                             "Добавить мероприятие"]

    def __init__(self, data_client: DataClient):
        self.data_client = data_client

    def check_announce_category(self, category_title: str) -> [bool, str]:
        if category_title:
            if not self.data_client.announce_category_exist(category_title):
                return [True, f"Название принято, теперь введите описание для категории."]
            else:
                return [False, "Такое название уже добавлено."]
        else:
            return [False, "Неккоректное название.\nПовторите"]

    def check_announce(self, announce_title: str) -> [bool, str]:
        if announce_title:
            if not self.data_client.announce_exist(announce_title):
                return [True, f"Название принято, теперь введите описание для мероприятия."]
            else:
                return [False, "Такое название уже добавлено."]
        else:
            return [False, "Неккоректное название.\nПовторите"]

    async def choice_option_announce_settings(self, msg: types.Message):
        back_msg = "Выберите, какую операцию хотите выполнить."
        await msg.answer(back_msg,
                         reply_markup=create_keyboards(self.btn_announce_settings, cancel_btn=True))
        await FSMWorkProgram.announce_settings_option.set()

    @staticmethod
    async def start_set_new_announce_category(msg: types.Message):
        await msg.answer("Введите название для новой категории.",
                         reply_markup=create_keyboards(list(), cancel_btn=True))
        await FSMWorkProgram.set_announce_category.set()

    async def set_announce_category_title(self, msg: types.Message, state: FSMContext):
        result = self.check_announce_category(msg.text)
        if result[0]:
            async with state.proxy() as data:
                data["category_title"] = msg.text
            await msg.answer(result[1])
            await FSMWorkProgram.set_announce_category_title.set()
        else:
            await msg.answer(result[1])

    @staticmethod
    async def set_announce_category_description(msg: types.Message, state: FSMContext):
        if len(msg.text) > 10:
            async with state.proxy() as data:
                data["description"] = msg.text
                back_msg = f"Сохранить следующую информацию?\nНазвание: {data['category_title']}\n" \
                           f"Описание: {msg.text}"
                await msg.answer(back_msg,
                                 reply_markup=create_keyboards(list(), yes_no_btn=True))
                await FSMWorkProgram.set_announce_category_description.set()
        else:
            await msg.answer("Неккоректное описание, повторите.")

    async def save_new_announce_category(self, msg: types.Message, state: FSMContext):
        if msg.text == "Да":
            async with state.proxy() as data:
                result = self.data_client.set_announce_category(title=data["category_title"],
                                                                description=data["description"])
            await msg.answer("Категория добавлена.",
                             reply_markup=create_keyboards(self.btn_announce_settings))
            await state.reset_data()
            await FSMWorkProgram.announce_settings_option.set()
        else:
            await msg.answer("Начнем с начала, введите другое название.",
                             reply_markup=create_keyboards(list(), cancel_btn=True))
            await state.reset_data()
            await FSMWorkProgram.set_announce_category.set()

    async def set_announce(self, msg: types.Message):
        category_btn = self.data_client.get_announce_category_list()[1]
        await msg.answer("Выберите категорию для нового мероприятия.",
                         reply_markup=create_keyboards(category_btn, cancel_btn=True))
        await FSMWorkProgram.set_announce.set()

    async def set_category_id(self, msg: types.Message, state: FSMContext):
        if self.data_client.announce_category_exist(msg.text):
            announce_category_id = self.data_client.get_announce_category_id(msg.text)
            async with state.proxy() as data:
                data["category_title"] = msg.text
                data["category_id"] = announce_category_id
            place_btn = self.data_client.get_all_place_list()[1]
            await msg.answer("Выберите в каком заведении проходит мероприятие.",
                             reply_markup=create_keyboards(place_btn, cancel_btn=True))
            await FSMWorkProgram.set_announce_category_id.set()
        else:
            await msg.answer("Нужно выбрать из предложенных вариантов.\nПовторите попытку")

    async def set_place_id(self, msg: types.Message, state: FSMContext):
        if self.data_client.place_exist(msg.text):
            async with state.proxy() as data:
                data["place_title"] = msg.text
                data["place_id"] = self.data_client.get_place_id(msg.text)
            await msg.answer("Введите название мероприятия.",
                             reply_markup=create_keyboards(list(), cancel_btn=True))
            await FSMWorkProgram.set_announce_place_id.set()
        else:
            await msg.answer("Выберите из предложенных вариантов.")

    async def set_announce_title(self, msg: types.Message, state: FSMContext):
        result = self.check_announce(msg.text)
        if result[0]:
            async with state.proxy() as data:
                data["announce_title"] = msg.text
            await msg.answer(result[1])
            await FSMWorkProgram.set_announce_title.set()
        else:
            await msg.answer(result[1])

    async def set_announce_description(self, msg: types.Message, state: FSMContext):
        if len(msg.text) > 10:
            async with state.proxy() as data:
                data["announce_description"] = msg.text
                await msg.answer("Введите стоимость мероприятия.")
                await FSMWorkProgram.set_announce_description.set()
        else:
            await msg.answer("Неккоректное значение, повторите.")

    async def set_announce_price(self, msg: types.Message, state: FSMContext):
        if len(msg.text) > 2:
            async with state.proxy() as data:
                data["price"] = msg.text
                await msg.answer("Введите ссылку на билет.")
                await FSMWorkProgram.set_announce_price.set()
        else:
            await msg.answer("Неккоректное значение, повторите.")

    async def set_announce_link_ticker(self, msg: types.Message, state: FSMContext):
        if len(msg.text) > 5:
            async with state.proxy() as data:
                data["ticker_link"] = msg.text
                await msg.answer("Введите дату мероприятия.")
                await FSMWorkProgram.set_announce_link_ticker.set()
        else:
            await msg.answer("Неккоректное значение, повторите.")

    async def set_announce_date(self, msg: types.Message, state: FSMContext):
        if len(msg.text) > 5:
            async with state.proxy() as data:
                data["date"] = msg.text
                await msg.answer("Введите время начала мероприятия.")
                await FSMWorkProgram.set_announce_date.set()
        else:
            await msg.answer("Неккоректное значение, повторите.")

    async def set_announce_time(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["time"] = msg.text
            await msg.answer("Время сохранено, теперь отправьте фотографию мероприятия.")
            await FSMWorkProgram.set_announce_time.set()

    async def set_announce_photo(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["photo"] = msg.photo[-1]["file_id"]
            back_msg = f"Сохранить следующую информацию?\nНазвание: {data['announce_title']}\n" \
                       f"Описание: {data['announce_description']}\nКатегория: {data['category_title']}\n" \
                       f"Заведение: {data['place_title']}\n" \
                       f"Цена: {data['price']}\nСсылка: {data['ticker_link']}\n" \
                       f"Дата: {data['date']}\nВремя: {data['time']}"
            await msg.answer_photo(data["photo"], back_msg,
                                   reply_markup=create_keyboards(list(), yes_no_btn=True))
            await FSMWorkProgram.set_announce_photo.set()

    async def save_new_announce(self, msg: types.Message, state: FSMContext):
        if msg.text == "Да":
            async with state.proxy() as data:
                result = self.data_client.set_announce(category_id=data["category_id"],
                                                       place_id=data["place_id"],
                                                       title=data["announce_title"],
                                                       description=data["announce_description"],
                                                       ticker_price=data["price"],
                                                       ticker_link=data["ticker_link"],
                                                       date=data["date"],
                                                       time_value=data["time"],
                                                       photo_id=data["photo"])
            if result:
                await msg.answer("Мероприятие добавлено.",
                                 reply_markup=create_keyboards(self.btn_admin_main_menu))
            else:
                await msg.answer("Произошла ошибка. Мероприятия не может быть добавлено.")
            await state.reset_data()
            await FSMWorkProgram.admin_main_menu.set()
            await state.reset_data()
        else:
            category_list = self.data_client.get_announce_category_list()
            await msg.answer("Начнем с начала, выберите категорию.",
                             reply_markup=create_keyboards(category_list, cancel_btn=True))
            await state.reset_data()
            await FSMWorkProgram.set_announce.set()

    def run_handler(self):
        dp.register_message_handler(self.choice_option_announce_settings,
                                    Text(equals="Настройки: мероприятия", ignore_case=True),
                                    state=FSMWorkProgram.admin_settings)

        # dp.register_message_handler(self.choice_option_announce_settings,
        #                             Text(equals="Добавить категорию", ignore_case=True),
        #                             state=FSMWorkProgram.admin_choice_settings_option)

        dp.register_message_handler(self.start_set_new_announce_category,
                                    Text(equals="Добавить категорию", ignore_case=True),
                                    state=FSMWorkProgram.announce_settings_option)
        dp.register_message_handler(self.set_announce_category_title,
                                    state=FSMWorkProgram.set_announce_category)
        dp.register_message_handler(self.set_announce_category_description,
                                    state=FSMWorkProgram.set_announce_category_title)
        dp.register_message_handler(self.save_new_announce_category,
                                    state=FSMWorkProgram.set_announce_category_description)

        dp.register_message_handler(self.set_announce,
                                    Text(equals="Добавить мероприятие", ignore_case=True),
                                    state=FSMWorkProgram.announce_settings_option)
        dp.register_message_handler(self.set_category_id,
                                    state=FSMWorkProgram.set_announce)
        dp.register_message_handler(self.set_place_id,
                                    state=FSMWorkProgram.set_announce_category_id)
        dp.register_message_handler(self.set_announce_title,
                                    state=FSMWorkProgram.set_announce_place_id)
        dp.register_message_handler(self.set_announce_description,
                                    state=FSMWorkProgram.set_announce_title)
        dp.register_message_handler(self.set_announce_price,
                                    state=FSMWorkProgram.set_announce_description)
        dp.register_message_handler(self.set_announce_link_ticker,
                                    state=FSMWorkProgram.set_announce_price)
        dp.register_message_handler(self.set_announce_date,
                                    state=FSMWorkProgram.set_announce_link_ticker)
        dp.register_message_handler(self.set_announce_time,
                                    state=FSMWorkProgram.set_announce_date)
        dp.register_message_handler(self.set_announce_photo,
                                    state=FSMWorkProgram.set_announce_time,
                                    content_types=["photo"])
        dp.register_message_handler(self.save_new_announce,
                                    state=FSMWorkProgram.set_announce_photo)
