from aiogram import types
from initial import bot, dp
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from dataClient.db_mysql import DataClient

from keyboards import create_keyboards
from config import FSMWorkProgram


class PlaceSettings:
    btn_admin_main_menu = ["Смотреть заведения",
                           "Найти заведение",
                           "Заведения рядом",
                           "Мероприятия",
                           "О проекте",
                           "Системные настройки"]
    btn_place_settings = ["Добавить категорию",
                          "Добавить заведение"]

    def __init__(self, data_client: DataClient):
        self.data_client = data_client

    def check_place_category(self, category_title: str) -> [bool, str]:
        if category_title:
            if not self.data_client.place_category_exist(category_title):
                return [True, f"Название принято, теперь введите описание для категории."]
            else:
                return [False, "Такое название уже добавлено."]
        else:
            return [False, "Неккоректное название.\nПовторите"]

    def check_place(self, place_title: str) -> [bool, str]:
        if place_title:
            if not self.data_client.place_exist(place_title):
                return [True, f"Название принято, теперь введите описание для заведения."]
            else:
                return [False, "Такое название уже добавлено."]
        else:
            return [False, "Неккоректное название.\nПовторите"]

    async def choice_option_place_settings(self, msg: types.Message):
        back_msg = "Выберите, какую операцию хотите выполнить."
        await msg.answer(back_msg,
                         reply_markup=create_keyboards(self.btn_place_settings, cancel_btn=True))
        await FSMWorkProgram.place_settings_option.set()

    @staticmethod
    async def start_set_new_place_category(msg: types.Message):
        await msg.answer("Введите название для новой категории.",
                         reply_markup=create_keyboards(list(), cancel_btn=True))
        await FSMWorkProgram.set_place_category.set()

    async def set_place_category_title(self, msg: types.Message, state: FSMContext):
        result = self.check_place_category(msg.text)
        if result[0]:
            async with state.proxy() as data:
                data["category_title"] = msg.text
            await msg.answer(result[1])
            await FSMWorkProgram.set_place_category_title.set()
        else:
            await msg.answer(result[1])

    @staticmethod
    async def set_place_category_description(msg: types.Message, state: FSMContext):
        if len(msg.text) > 10:
            async with state.proxy() as data:
                data["description"] = msg.text
                back_msg = f"Сохранить следующую информацию?\nНазвание: {data['category_title']}\n" \
                           f"Описание: {msg.text}"
                await msg.answer(back_msg,
                                 reply_markup=create_keyboards(list(), yes_no_btn=True))
                await FSMWorkProgram.set_place_category_description.set()
        else:
            await msg.answer("Неккоректное описание, повторите.")

    async def save_new_place_category(self, msg: types.Message, state: FSMContext):
        if msg.text == "Да":
            async with state.proxy() as data:
                result = self.data_client.set_place_category(title=data["category_title"],
                                                             description=data["description"])
            await msg.answer("Категория добавлена.",
                             reply_markup=create_keyboards(self.btn_place_settings))
            await state.reset_data()
            await FSMWorkProgram.place_settings_option.set()
        else:
            await msg.answer("Начнем с начала, введите другое название.",
                             reply_markup=create_keyboards(list(), cancel_btn=True))
            await state.reset_data()
            await FSMWorkProgram.set_place_category.set()

    async def set_place(self, msg: types.Message):
        category_btn = self.data_client.get_place_category_list()[1]
        await msg.answer("Выберите категорию для нового места.",
                         reply_markup=create_keyboards(category_btn, cancel_btn=True))
        await FSMWorkProgram.set_place.set()

    async def set_category_id(self, msg: types.Message, state: FSMContext):
        if self.data_client.place_category_exist(msg.text):
            place_category_id = self.data_client.get_place_category_id(msg.text)
            async with state.proxy() as data:
                data["category_title"] = msg.text
                data["category_id"] = place_category_id
            await msg.answer("Введите название заведения",
                             reply_markup=create_keyboards(list(), cancel_btn=True))
            await FSMWorkProgram.set_place_category_id.set()
        else:
            await msg.answer("Нужно выбрать из предложенных вариантов.\nПовторите попытку")

    async def set_place_title(self, msg: types.Message, state: FSMContext):
        result = self.check_place(msg.text)
        if result[0]:
            async with state.proxy() as data:
                data["place_title"] = msg.text
            await msg.answer(result[1])
            await FSMWorkProgram.set_place_title.set()
        else:
            await msg.answer(result[1])

    async def set_place_description(self, msg: types.Message, state: FSMContext):
        if len(msg.text) > 10:
            async with state.proxy() as data:
                data["place_description"] = msg.text
                await msg.answer("Введите адрес заведения")
                await FSMWorkProgram.set_place_description.set()
        else:
            await msg.answer("Неккоректное название, повторите.")

    async def set_place_address(self, msg: types.Message, state: FSMContext):
        if len(msg.text) > 5:
            async with state.proxy() as data:
                data["place_address"] = msg.text
                await msg.answer("Введите ссылку на сайт заведения..")
                await FSMWorkProgram.set_place_address.set()
        else:
            await msg.answer("Неккоректное начение, повторите.")

    async def set_place_site_link(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["place_site"] = msg.text
            await msg.answer("Отправьте фото заведения.")
            await FSMWorkProgram.set_place_site_link.set()

    async def set_place_photo(self, msg: types.Message, state: FSMContext):
        if msg.content_type != "photo":
            await msg.answer("Необходимо фото. Повторите попытку.")
        else:
            async with state.proxy() as data:
                data["place_photo"] = msg.photo[-1]["file_id"]
            await msg.answer("Введите контакт заведения.")
            await FSMWorkProgram.set_place_photo.set()

    async def set_place_contact(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["place_contact"] = msg.text
            await msg.answer("Введите время работы заведения.")
            await FSMWorkProgram.set_place_contact.set()

    async def set_place_work_time(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["place_work_time"] = msg.text
            back_msg = f"Сохранить следующую информацию?\nНазвание: {data['place_title']}\n" \
                       f"Описание: {data['place_description']}\nКатегория: {data['category_title']}\n" \
                       f"Адрес: {data['place_address']}\nСайт: {data['place_site']}\n" \
                       f"Контакт: {data['place_contact']}\nВремя работы: {data['place_work_time']}"
            await msg.answer_photo(data["place_photo"], back_msg,
                                   reply_markup=create_keyboards(list(), yes_no_btn=True))

            await FSMWorkProgram.set_place_work_time.set()

    async def save_new_place(self, msg: types.Message, state: FSMContext):
        if msg.text == "Да":
            async with state.proxy() as data:
                result = self.data_client.set_place(title=data["place_title"],
                                                    description=data["place_description"],
                                                    category_id=data["category_id"],
                                                    address=data["place_address"],
                                                    site=data["place_site"],
                                                    contact=data["place_contact"],
                                                    work_time=data["place_work_time"],
                                                    photo_id=data["place_photo"])
            if result:
                await msg.answer("Заведение добавлено.",
                                 reply_markup=create_keyboards(self.btn_admin_main_menu))
            else:
                await msg.answer("Произошла ошибка, сейчас нельзя добавить новое заведение.",
                                 reply_markup=create_keyboards(self.btn_admin_main_menu))
            await state.reset_data()
            await FSMWorkProgram.admin_main_menu.set()
            await state.reset_data()
        else:
            category_list = self.data_client.get_place_category_list()
            await msg.answer("Начнем с начала, выберите категорию.",
                             reply_markup=create_keyboards(category_list, cancel_btn=True))
            await state.reset_data()
            await FSMWorkProgram.set_place.set()

    def run_handler(self):
        dp.register_message_handler(self.choice_option_place_settings,
                                    Text(equals="Настройки: заведения", ignore_case=True),
                                    state=FSMWorkProgram.admin_settings)

        # dp.register_message_handler(self.choice_option_place_settings,
        #                             Text(equals="Добавить категорию", ignore_case=True),
        #                             state=FSMWorkProgram.admin_choice_settings_option)

        dp.register_message_handler(self.start_set_new_place_category,
                                    Text(equals="Добавить категорию", ignore_case=True),
                                    state=FSMWorkProgram.place_settings_option)
        dp.register_message_handler(self.set_place_category_title,
                                    state=FSMWorkProgram.set_place_category)
        dp.register_message_handler(self.set_place_category_description,
                                    state=FSMWorkProgram.set_place_category_title)
        dp.register_message_handler(self.save_new_place_category,
                                    state=FSMWorkProgram.set_place_category_description)

        dp.register_message_handler(self.set_place,
                                    Text(equals="Добавить заведение", ignore_case=True),
                                    state=FSMWorkProgram.place_settings_option)
        dp.register_message_handler(self.set_category_id,
                                    state=FSMWorkProgram.set_place)
        dp.register_message_handler(self.set_place_title,
                                    state=FSMWorkProgram.set_place_category_id)
        dp.register_message_handler(self.set_place_description,
                                    state=FSMWorkProgram.set_place_title)
        dp.register_message_handler(self.set_place_address,
                                    state=FSMWorkProgram.set_place_description)
        dp.register_message_handler(self.set_place_site_link,
                                    state=FSMWorkProgram.set_place_address)
        dp.register_message_handler(self.set_place_photo,
                                    state=FSMWorkProgram.set_place_site_link,
                                    content_types=["photo"])
        dp.register_message_handler(self.set_place_contact,
                                    state=FSMWorkProgram.set_place_photo)
        dp.register_message_handler(self.set_place_work_time,
                                    state=FSMWorkProgram.set_place_contact)
        dp.register_message_handler(self.save_new_place,
                                    state=FSMWorkProgram.set_place_work_time)


