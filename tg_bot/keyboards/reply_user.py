from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def start_keyboard_worker():
    """Главное Меню Воркера"""
    button_my_chats = KeyboardButton('💬 Мои Чаты')
    menu = ReplyKeyboardMarkup(resize_keyboard=True)
    menu.row(button_my_chats)
    return menu


def send_message_keyboard_worker():
    """Клавиатура При Отправке Сообщения Воркером"""
    button_disconnect = KeyboardButton('❌ Отсоединиться')
    menu = ReplyKeyboardMarkup(resize_keyboard=True)
    menu.row(button_disconnect)
    return menu
