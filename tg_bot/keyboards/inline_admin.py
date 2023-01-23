from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_menu_admin():
    """Главное Меню Админа"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    mammoth = InlineKeyboardButton('🦣 Мамонты', callback_data='My mammoth')
    wallets = InlineKeyboardButton('💼 Кошельки', callback_data='My wallets')
    settings = InlineKeyboardButton('⚙️ Настройка', callback_data='Settings Admin')
    
    buttons \
    .add(mammoth) \
    .add(wallets) \
    .add(settings)
    return buttons


def back_main_menu_admin():
    """Назад в Главное Меню Админа"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Main Menu Admin')
    
    buttons.add(back)
    return buttons


def my_wallets_menu_admin():
    """Мои Кошельки Админа"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    show_my_wallets = InlineKeyboardButton('💼 Посмотреть Кошельки', callback_data='Show My Wallets')
    change_btc = InlineKeyboardButton('✏️ Изменить Bitcoin', callback_data='Change My Bitcoin Wallet')
    change_ltc = InlineKeyboardButton('✏️ Изменить Litecoin', callback_data='Change My Litecoin Wallet')
    change_sber = InlineKeyboardButton('✏️ Изменить Сбербанк', callback_data='Change My Sberbank Card')
    change_visa = InlineKeyboardButton('✏️ Изменить Visa', callback_data='Change My Visa Card')
    back = InlineKeyboardButton('« Назад', callback_data='Main Menu Admin')
    
    buttons \
    .add(show_my_wallets) \
    .add(change_btc) \
    .add(change_ltc) \
    .add(change_sber) \
    .add(change_visa) \
    .add(back)
    return buttons


def back_wallets_menu_admin():
    """Назад в Кошельки Меню Админа"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='My wallets')
    
    buttons.add(back)
    return buttons


def cancel_change_btc_wallet_menu_admin():
    """Отмена Изменения Bitcoin Кошелька Меню Админа"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Cancel Change Bitcoin wallet')
    
    buttons.add(back)
    return buttons


def cancel_change_ltc_wallet_menu_admin():
    """Отмена Изменения Litecoin Кошелька Меню Админа"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Cancel Change Litecoin wallet')
    
    buttons.add(back)
    return buttons


def cancel_change_sber_wallet_menu_admin():
    """Отмена Изменения Sberbank Кошелька Меню Админа"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Cancel Change Sberbank wallet')
    
    buttons.add(back)
    return buttons


def cancel_change_visa_wallet_menu_admin():
    """Отмена Изменения Visa Кошелька Меню Админа"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Cancel Change Visa wallet')
    
    buttons.add(back)
    return buttons


def settings_menu_admin():
    """Настройки магазина - Админа"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    show_percent = InlineKeyboardButton('🔍 Посмотреть %', callback_data='Show Percent Admin')
    change_percent = InlineKeyboardButton('✏️ Изменить %', callback_data='Change Percent Admin')
    back = InlineKeyboardButton('« Назад', callback_data='Main Menu Admin')
    
    buttons.add(show_percent, change_percent).add(back)
    return buttons


def back_settings_menu_admin():
    """Назад в Настройки Меню Админа"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Settings Admin')
    
    buttons.add(back)
    return buttons


def cancel_change_percent_settings_menu_admin():
    """Отмена Настройки Процента Магазина - Меню Админа"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Cancel Change Percent Admin')
    
    buttons.add(back)
    return buttons
