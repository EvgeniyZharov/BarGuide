from aiogram import types
from initial import bot, dp
from keyboards import create_keyboards
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from dataClient.db_mysql import DataClient
from config import FSMWorkProgram


class BaseChoicePlace:
    function_for_place = ["Открыть меню",
                          "Смотреть отзывы",
                          "Смотреть мероприятия",
                          "Оставить отзыв",
                          "Забронировать",
                          "Краткое описание",
                          "Контакт",
                          "Сайт"]

    def __init__(self, data_client: DataClient) -> None:
        self.data_client = data_client

    async def choice_place(self, msg: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            place_info = self.data_client.get_place_info(msg.text)
            place_id = place_info["id"]
            data["place_id"] = place_id
        back_msg = f"{place_info['title']}\n\nАдрес: {place_info['address']}\n" \
                   f"Время работы: {place_info['work_time']}\nРейтинг: {place_info['rating']}\n"
        await msg.answer_photo(place_info["photo_id"], back_msg,
                               reply_markup=create_keyboards(self.function_for_place, cancel_btn=True))
        await FSMWorkProgram.choice_place.set()

    async def get_place_menu(self, msg: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            place_id = data["place_id"]
            meal_list = self.data_client.get_meal_list(place_id=place_id)
        if meal_list[0]:
            await msg.reply("Выберите позицию.",
                            reply_markup=create_keyboards(meal_list[1], cancel_btn=True))
            await FSMWorkProgram.get_menu.set()
        else:
            await msg.reply("Скоро в меню добавят блюда.")

    async def get_meal_info(self, msg: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            place_id = data["place_id"]
        meal_info = self.data_client.get_meal_info(title=msg.text, place_id=place_id)
        back_msg = f"{meal_info['title']}\n{meal_info['description']}\n" \
                   f"Composition: {meal_info['composition']}\n\n{meal_info['price']} руб."
        await msg.reply(back_msg)

    async def get_place_reviews(self, msg: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            place_id = data["place_id"]
        reviews = self.data_client.get_all_place_review(place_id=place_id)
        if reviews[0]:
            for elem in reviews[1]:
                back_msg = f"{elem['user_name']}\nRating: {elem['rating']}\n" \
                           f"{elem['text']}"
                await msg.answer(back_msg)
        else:
            await msg.reply("Пока отзывов нет.")

    async def get_place_announces(self, msg: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            place_id = data["place_id"]
        announces = self.data_client.get_place_announce(place_id)
        if announces[0]:
            await msg.answer("Выберите мероприятие, которое Вас интересует.",
                             reply_markup=create_keyboards(announces[1], cancel_btn=True))
            await FSMWorkProgram.get_announces.set()
        else:
            await msg.answer("В ближейшее время не намечается мероприятий.")

    async def get_announce(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            place_id = data["place_id"]
        announce_info = self.data_client.get_announce_info_for_place(title=msg.text, place_id=place_id)
        back_msg = f"{announce_info['title']}\n{announce_info['description']}\n\n" \
                   f"Ticker price: {announce_info['price']} руб.\nLink for paying: {announce_info['link_ticker']}"
        await msg.reply(back_msg)

    async def set_new_review(self, msg: types.Message) -> None:
        await msg.answer("Выберите оценку для этого заведения.",
                         reply_markup=create_keyboards([1, 2, 3, 4, 5], cancel_btn=True))
        await FSMWorkProgram.set_review_rating.set()

    async def set_text_for_review(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["place_rating"] = msg.text
        await msg.answer("Введите текст для отзыва заведению.",
                         reply_markup=create_keyboards(list(), cancel_btn=True))
        await FSMWorkProgram.set_review_text.set()

    async def save_new_review(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            rating = data["place_rating"]
            place_id = data["place_id"]
        user_name = msg.from_user.full_name
        user_link = msg.from_user.id
        result = self.data_client.set_review(place_id=place_id,
                                             user_name=user_name,
                                             user_id=user_link,
                                             text=msg.text,
                                             rating=rating)
        if result:
            await msg.answer("Ваш отзыв сохранен.",
                             reply_markup=create_keyboards(self.function_for_place, cancel_btn=True))
        else:
            await msg.answer("Произошла ошибка.",
                             reply_markup=create_keyboards(self.function_for_place, cancel_btn=True))
        await FSMWorkProgram.choice_place.set()

    async def set_name_reserve(self, msg: types.Message) -> None:
        await msg.answer("Введите Ваше имя, чтобы оформить бронь.",
                         reply_markup=create_keyboards(list(), cancel_btn=True))
        await FSMWorkProgram.set_name_reservist.set()

    async def set_phone_reservist(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["user_name"] = msg.text
        set_phone_btn = ReplyKeyboardMarkup(resize_keyboard=True)
        set_phone_btn.add(KeyboardButton("Поделиться номером телефона", request_contact=True))
        set_phone_btn.add(KeyboardButton("Отмена"))
        await msg.answer(f"{msg.text}, нажмите на кнопку, чтобы записать Ваш телефон для связи.",
                         reply_markup=set_phone_btn)
        await FSMWorkProgram.set_phone_reservist.set()

    async def set_data_reserve(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["user_phone"] = msg.contact.phone_number
        await msg.answer("Введите дату, в которую собираетесь прийти.",
                         reply_markup=create_keyboards(list(), cancel_btn=True))
        await FSMWorkProgram.set_date_reserve.set()

    async def set_time_reserve(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["date_reserve"] = msg.text
        await msg.answer("Введите время визита")
        await FSMWorkProgram.set_time_reserve.set()

    async def save_data_reserve(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            result = self.data_client.set_new_reserve(place_id=data["place_id"],
                                                      user_name=data["user_name"],
                                                      user_link=msg.from_user.id,
                                                      date=data["date_reserve"],
                                                      time=msg.text,
                                                      user_number=data["user_phone"])
            if result:
                await msg.answer("Ваше бронирование сохранено.",
                                 reply_markup=create_keyboards(self.function_for_place, cancel_btn=True))
            else:
                await msg.answer("Произошла ошибка.",
                                 reply_markup=create_keyboards(self.function_for_place, cancel_btn=True))
            await FSMWorkProgram.choice_place.set()

    async def get_place_description(self, msg: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            place_id = data["place_id"]
        result = self.data_client.get_place_description(place_id=place_id)
        await msg.reply(result)

    async def get_place_contact(self, msg: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            place_id = data["place_id"]
        result = self.data_client.get_place_contact(place_id=place_id)
        await msg.reply(result)

    async def get_place_site(self, msg: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            place_id = data["place_id"]
        result = self.data_client.get_place_site(place_id=place_id)
        await msg.reply(result)

    def run_handler(self) -> None:
        dp.register_message_handler(self.choice_place,
                                    state=FSMWorkProgram.get_place)

        dp.register_message_handler(self.get_place_menu,
                                    Text(equals="Открыть меню", ignore_case=True),
                                    state=FSMWorkProgram.choice_place)
        dp.register_message_handler(self.get_meal_info,
                                    state=FSMWorkProgram.get_menu)

        dp.register_message_handler(self.get_place_reviews,
                                    Text(equals="Смотреть отзывы", ignore_case=True),
                                    state=FSMWorkProgram.choice_place)

        dp.register_message_handler(self.get_place_announces,
                                    Text(equals="Смотреть мероприятия", ignore_case=True),
                                    state=FSMWorkProgram.choice_place)
        dp.register_message_handler(self.get_announce,
                                    state=FSMWorkProgram.get_announces)

        dp.register_message_handler(self.set_new_review,
                                    Text(equals="Оставить отзыв", ignore_case=True),
                                    state=FSMWorkProgram.choice_place)
        dp.register_message_handler(self.set_text_for_review,
                                    state=FSMWorkProgram.set_review_rating)
        dp.register_message_handler(self.save_new_review,
                                    state=FSMWorkProgram.set_review_text)

        dp.register_message_handler(self.set_name_reserve,
                                    Text(equals="Забронировать", ignore_case=True),
                                    state=FSMWorkProgram.choice_place)
        dp.register_message_handler(self.set_phone_reservist,
                                    state=FSMWorkProgram.set_name_reservist)
        dp.register_message_handler(self.set_data_reserve,
                                    content_types=["contact"],
                                    state=FSMWorkProgram.set_phone_reservist)
        dp.register_message_handler(self.set_time_reserve,
                                    state=FSMWorkProgram.set_date_reserve)
        dp.register_message_handler(self.save_data_reserve,
                                    state=FSMWorkProgram.set_time_reserve)

        dp.register_message_handler(self.get_place_description,
                                    Text(equals="Краткое описание", ignore_case=True),
                                    state=FSMWorkProgram.choice_place)

        dp.register_message_handler(self.get_place_contact,
                                    Text(equals="Контакт", ignore_case=True),
                                    state=FSMWorkProgram.choice_place)

        dp.register_message_handler(self.get_place_site,
                                    Text(equals="Сайт", ignore_case=True),
                                    state=FSMWorkProgram.choice_place)
