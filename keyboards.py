from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_keyboards(btn_list, cancel_btn=False, back_btn=False,
                     yes_no_btn=False):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for elem in btn_list:
        kb.add(KeyboardButton(elem))
    if yes_no_btn:
        kb.add(KeyboardButton("Да"))
        kb.add(KeyboardButton("Нет"))
    if cancel_btn:
        kb.add(KeyboardButton("Отмена"))
    if back_btn:
        kb.add(KeyboardButton("Назад"))

    return kb


def create_start_btn():
    btns = ["Смотреть заведения", "Найти заведение", "Заведения рядом", "Смотреть анонсы", "О проекте"]
    return create_keyboards(btns)
