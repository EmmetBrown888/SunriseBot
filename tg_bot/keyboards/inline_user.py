from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.text.user import service_chat, service_channel, website_chat, operator_support, reviews_channel
from database.database import get_code_word, get_reviews, get_active_commission_crypto

from datetime import datetime


def main_menu_user():
    """Главное Меню Воркера"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    buy = InlineKeyboardButton('↙️ Купить', callback_data='Buy')
    sell = InlineKeyboardButton('↗️ Продать', callback_data='Sell')
    wallet = InlineKeyboardButton('👛 Кошелёк', callback_data='Wallet')
    refferal = InlineKeyboardButton('👥 Рефералка', callback_data='Refferal')
    lottery = InlineKeyboardButton('🎰 Лотерея', callback_data='Lottery')
    my_cabinet = InlineKeyboardButton('🗄 Мой кабинет', callback_data='My Personal Cabinet')
    practical_jokes = InlineKeyboardButton('🤑 Розыгрыши', callback_data='Practical jokes')
    site = InlineKeyboardButton('🌐 Сайт', url=website_chat)
    channel = InlineKeyboardButton('📢 Канал', url=f'https://t.me/{service_channel}')
    reviews = InlineKeyboardButton('📝 Отзывы', callback_data='Reviews')
    operator = InlineKeyboardButton('🆘 Оператор', url=f'https://t.me/{operator_support}')
    info = InlineKeyboardButton('ℹ️ Инфо', callback_data='Info')
    
    buttons \
    .add(buy, sell) \
    .add(wallet, refferal) \
    .add(lottery, my_cabinet) \
    .add(practical_jokes) \
    .add(site, channel) \
    .add(reviews) \
    .add(operator, info)
    return buttons

# =============================================== Купить ================================================ #
def buy_crypto_menu_user():
    """Купить Раздел"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    bitcoin = InlineKeyboardButton('Bitcoin', callback_data='Buy Bitcoin')
    litecoin = InlineKeyboardButton('Litecoin', callback_data='Buy Litecoin')
    back = InlineKeyboardButton('« Назад', callback_data='Main Menu')
    
    buttons \
    .add(bitcoin) \
    .add(litecoin) \
    .add(back)
    return buttons

def cancel_enter_buy_crypto_menu_user():
    """Отмена Ввода суммы покупки крипты"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Cancel Buy CryptoCurrency')
    
    buttons.add(back)
    return buttons


def back_buy_crypto_menu_user():
    """Отмена Ввода суммы покупки крипты"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Buy')
    
    buttons.add(back)
    return buttons


def cancel_enter_crypto_wallet_menu_user():
    """Отмена Ввода Криптовалютного Кошелька"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Cancel Enter Crypto Wallet')
    
    buttons.add(back)
    return buttons

def info_detail_min_commission_crypto_buy_menu_user():
    """Информация о Покупки Крипты - Минимальная Коммиссия"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    min_commission = InlineKeyboardButton('🐌 Минимальная:✅', callback_data='Min Commission')
    average_commission = InlineKeyboardButton('⚖️ Средняя:☑️(+23₽)', callback_data='Average Commission')
    high_commission = InlineKeyboardButton('🚀 Высокая:☑️(+75₽)', callback_data='High Commission')
    cont_commission = InlineKeyboardButton('➡️ Продолжить', callback_data='Continue Commission')
    back = InlineKeyboardButton('« Назад', callback_data='Buy')
    
    buttons \
        .add(min_commission) \
        .add(average_commission) \
        .add(high_commission) \
        .add(cont_commission) \
        .add(back)
    return buttons


async def info_detail_average_commission_crypto_buy_menu_user(user_id):
    """Информация о Покупки Крипты - Средняя Коммиссия"""
    amount_commission = await get_active_commission_crypto(user_id)
    
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    min_commission = InlineKeyboardButton(f'🐌 Минимальная:☑️(-{amount_commission}₽)', callback_data='Min Commission')
    average_commission = InlineKeyboardButton('⚖️ Средняя:✅', callback_data='Average Commission')
    high_commission = InlineKeyboardButton('🚀 Высокая:☑️(+52₽)', callback_data='High Commission')
    cont_commission = InlineKeyboardButton('➡️ Продолжить', callback_data='Continue Commission')
    back = InlineKeyboardButton('« Назад', callback_data='Buy')
    
    buttons \
        .add(min_commission) \
        .add(average_commission) \
        .add(high_commission) \
        .add(cont_commission) \
        .add(back)
    return buttons


async def info_detail_high_commission_crypto_buy_menu_user(user_id):
    """Информация о Покупки Крипты - Высокая Коммиссия"""
    amount_commission = await get_active_commission_crypto(user_id)
    
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    min_commission = InlineKeyboardButton(f'🐌 Минимальная:☑️(-{amount_commission}₽)', callback_data='Min Commission')
    average_commission = InlineKeyboardButton('⚖️ Средняя:☑️(-52₽)', callback_data='Average Commission')
    high_commission = InlineKeyboardButton('🚀 Высокая:✅', callback_data='High Commission')
    cont_commission = InlineKeyboardButton('➡️ Продолжить', callback_data='Continue Commission')
    back = InlineKeyboardButton('« Назад', callback_data='Buy')
    
    buttons \
        .add(min_commission) \
        .add(average_commission) \
        .add(high_commission) \
        .add(cont_commission) \
        .add(back)
    return buttons


def continue_crypto_buy_menu_user():
    """Информация о Покупки Крипты - Выбор способа оплаты"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    sberbank = InlineKeyboardButton('🟢 Сбербанк', callback_data='Main Buy Crypto Sberbank')
    card = InlineKeyboardButton('💳 Visa/MasterCard', callback_data='Main Buy Crypto Visa')
    back = InlineKeyboardButton('« Отмена', callback_data='Buy')
    
    buttons.add(sberbank, card).add(back)
    return buttons

# =============================================== Продать ================================================ #
def sell_crypto_menu_user():
    """Продать Раздел"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    bitcoin = InlineKeyboardButton('Bitcoin', callback_data='Sell Bitcoin')
    litecoin = InlineKeyboardButton('Litecoin', callback_data='Sell Litecoin')
    back = InlineKeyboardButton('« Назад', callback_data='Main Menu')
    
    buttons \
    .add(bitcoin) \
    .add(litecoin) \
    .add(back)
    return buttons

def sell_enter_amount_menu_user():
    """Продать Раздел - Написание цены продажи"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Cancel Sell CryptoCurrency')
    
    buttons.add(back)
    return buttons

def sell_continue_menu_user():
    """Продать Раздел - Продолжить"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    continue_sell = InlineKeyboardButton('✅ Продолжить', callback_data='Continue Sell CryptoCurrency')
    back = InlineKeyboardButton('« Назад', callback_data='Sell')
    
    buttons.add(continue_sell).add(back)
    return buttons

def sell_enter_card_menu_user():
    """Продать Раздел - Написание Банковской карты"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Cancel Sell CryptoCurrency Enter Card')
    
    buttons.add(back)
    return buttons

def sell_continue_menu_user_2():
    """Продать Раздел - Продолжить 2"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    continue_sell = InlineKeyboardButton('✅ Подтвердить', callback_data='Continue Sell CryptoCurrency 2')
    back = InlineKeyboardButton('« Назад', callback_data='Sell')
    
    buttons.add(continue_sell).add(back)
    return buttons
# =============================================== Кошелёк =============================================== #
def wallet_menu_user():
    """Кошелёк раздел"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    ruble = InlineKeyboardButton('Рубль', callback_data='Choose Ruble Wallet')
    bitcoin = InlineKeyboardButton('Bitcoin', callback_data='Choose Bitcoin Wallet')
    litecoin = InlineKeyboardButton('Litecoin', callback_data='Choose Litecoin Wallet')
    voucher = InlineKeyboardButton('🎟 Ввести ваучер', callback_data='Write Voucher')
    currency_converter = InlineKeyboardButton('♻️ Конвертер валют', callback_data='Converter Currency')
    back = InlineKeyboardButton('« Назад', callback_data='Main Menu')
    
    buttons \
    .add(ruble, bitcoin) \
    .add(litecoin) \
    .add(voucher) \
    .add(currency_converter) \
    .add(back)
    return buttons


def choose_ruble_wallet_menu_user():
    """Кошелек Рубль выбраный"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    lottery = InlineKeyboardButton('🎰 Лотерея', callback_data='Lottery')
    out_money = InlineKeyboardButton('📤 Вывод средств', callback_data='Out money Ruble')
    send_to_friend = InlineKeyboardButton('💸 Перевести другу', callback_data='Send Ruble To Friend')
    currency_converter = InlineKeyboardButton('♻️ Конвертер валют', callback_data='Converter Currency')
    back = InlineKeyboardButton('« Назад', callback_data='Wallet')
    
    buttons \
    .add(lottery) \
    .add(out_money, send_to_friend) \
    .add(currency_converter) \
    .add(back)
    return buttons


def choose_crypto_wallet_menu_user():
    """Кошелек Crypto выбраный"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    add_balance = InlineKeyboardButton('💰 Пополнить баланс', callback_data='Add Balance')
    out_money_card = InlineKeyboardButton('💳 Вывести на карту', callback_data='Out to Card')
    send = InlineKeyboardButton('📤 Отправить', callback_data='Send')
    voucher = InlineKeyboardButton('🎟 Создать ваучер', callback_data='Create Voucher')
    link_add = InlineKeyboardButton('💸 Ссылки на пополнение', callback_data='Link to add')
    currency_converter = InlineKeyboardButton('♻️ Конвертер валют', callback_data='Converter Currency')
    back = InlineKeyboardButton('« Назад', callback_data='Wallet')
    
    buttons \
    .add(add_balance) \
    .add(out_money_card) \
    .add(send) \
    .add(voucher) \
    .add(link_add) \
    .add(currency_converter) \
    .add(back)
    return buttons


def converter_currency():
    """Конвертер Валют"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Wallet')
    
    buttons.add(back)
    return buttons


def write_voucher_currency():
    """Написать Ваучер"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Wallet')
    
    buttons.add(back)
    return buttons


def add_balance_currency():
    """Пополнить баланс"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Cancel')
    
    buttons.add(back)
    return buttons


def method_pay_buy_crypto():
    """Выбор метода пополнение Крипты"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    sberbank = InlineKeyboardButton('🟢 Сбербанк', callback_data='Buy Crypto Sberbank')
    card = InlineKeyboardButton('💳 Visa/MasterCard', callback_data='Buy Crypto Visa')
    back = InlineKeyboardButton('« Отмена', callback_data='Wallet')
    
    buttons.add(sberbank, card).add(back)
    return buttons


def create_bid_crypto():
    """Созданая заявка"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    paid = InlineKeyboardButton('✅ Я оплатил(а)', callback_data='Main Menu')
    cancel = InlineKeyboardButton('❌Отменить заявку', callback_data='Main Menu')
    
    buttons.add(paid, cancel)
    return buttons


def create_link_voucher_currency_keyboard():
    """Создать ссылку Для пополнения"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Wallet')
    
    buttons.add(back)
    return buttons
# =============================================== Рефералка =============================================== #
def refferal_menu_user():
    """Реферальный раздел"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    invite_friend = InlineKeyboardButton('👤Пригласить друга', callback_data='Main Menu')
    lottery = InlineKeyboardButton('🎰 Лотерея', callback_data='Lottery')
    out_money = InlineKeyboardButton('📤 Вывод средств', callback_data='Out money')
    send_to_friend = InlineKeyboardButton('💸 Перевести другу', callback_data='Send Money To Friend')
    back = InlineKeyboardButton('« Назад', callback_data='Main Menu')
    
    buttons \
    .add(invite_friend) \
    .add(lottery) \
    .add(out_money, send_to_friend) \
    .add(back)
    return buttons


def refferal_back_menu_user():
    """Розыгрыши раздел - Вывод средств"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Refferal')
    
    buttons.add(back)
    return buttons

# =============================================== Лотерея =============================================== #
def lottery_menu_user():
    """Лотерея раздел"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Main Menu')
    
    buttons.add(back)
    return buttons


# =============================================== Мой Кабинет =============================================== #
def my_personal_cabinet_menu_user():
    """Мой Кабинет раздел"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    detailed_statistics = InlineKeyboardButton('➕ Подробная статистика', callback_data='Detailed statistics')
    code_word = InlineKeyboardButton('🔒 Кодовое слово', callback_data='Code Word')
    history_exchange = InlineKeyboardButton('📋 История обменов', callback_data='History Exchanges')
    enter_promocode = InlineKeyboardButton('🎫 Ввести промокод', callback_data='Enter promo code')
    back = InlineKeyboardButton('« Назад', callback_data='Main Menu')
    
    buttons \
    .add(detailed_statistics) \
    .add(code_word) \
    .add(history_exchange) \
    .add(enter_promocode) \
    .add(back)
    return buttons


def detail_stats_cabinet_menu_user():
    """Детальная статистика"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    detailed_statistics = InlineKeyboardButton('➖ Краткая статистика', callback_data='Brief statistics')
    code_word = InlineKeyboardButton('🔒 Кодовое слово', callback_data='Code Word')
    history_exchange = InlineKeyboardButton('📋 История обменов', callback_data='History Exchanges')
    enter_promocode = InlineKeyboardButton('🎫 Ввести промокод', callback_data='Enter promo code')
    back = InlineKeyboardButton('« Назад', callback_data='Main Menu')
    
    buttons \
    .add(detailed_statistics) \
    .add(code_word) \
    .add(history_exchange) \
    .add(enter_promocode) \
    .add(back)
    return buttons


def history_exchanges_menu_user():
    """История обменов раздел"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='My Personal Cabinet')
    
    buttons.add(back)
    return buttons


async def code_word_menu_user(user_id):
    """Кодовое слово раздел"""
    code_word = await get_code_word(user_id)
    if code_word:
        buttons = InlineKeyboardMarkup(resize_keyboard=True)
        set_word = InlineKeyboardButton('❌ Удалить слово', callback_data='Delete Code Word')
        back = InlineKeyboardButton('« Назад', callback_data='My Personal Cabinet')
        
        buttons.add(set_word).add(back)
        return buttons
    else:
        buttons = InlineKeyboardMarkup(resize_keyboard=True)
        set_word = InlineKeyboardButton('✅ Установить слово', callback_data='Set Code Word')
        back = InlineKeyboardButton('« Назад', callback_data='My Personal Cabinet')
        
        buttons.add(set_word).add(back)
        return buttons


def cancel_set_code_menu_user():
    """История обменов раздел"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Cancel Code Word')
    
    buttons.add(back)
    return buttons


def display_code_menu_user():
    """История обменов раздел"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    approve = InlineKeyboardButton('✅ Да', callback_data='Approve Code Word')
    skip = InlineKeyboardButton('➡️ Пропустить', callback_data='Skip Code Word')
    back = InlineKeyboardButton('« Назад', callback_data='Code Word Dont Set')
    
    buttons.add(approve, skip).add(back)
    return buttons


def skip_code_menu_user():
    """История обменов раздел"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Code Word')
    
    buttons.add(back)
    return buttons


def remove_code_menu_user():
    """История обменов раздел"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Remove Code Word')
    
    buttons.add(back)
    return buttons


def cancel_add_code_menu_user():
    """История обменов раздел"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Cancel Add Help Text Word')
    
    buttons.add(back)
    return buttons
# =============================================== Розыгрыши =============================================== #
def practical_jokes_menu_user():
    """Розыгрыши раздел"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    luckiest_jokes = InlineKeyboardButton('🍀Самый везучий 777₽', callback_data='The luckiest')
    back = InlineKeyboardButton('« Назад', callback_data='Main Menu')
    
    buttons \
    .add(luckiest_jokes) \
    .add(back)
    return buttons


def practical_jokes_back_menu_user():
    """Розыгрыши раздел - Самый Везучий"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Practical jokes')
    
    buttons.add(back)
    return buttons

# ====================================================== Отзывы ======================================================= #
async def reviews_menu_user():
    """Отзывы раздел"""
    reviews = await get_reviews()
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    for review in reviews:
        author = f'📅 {datetime.today().strftime("%d-%m-%Y")} | 👤 {review[1]}'
        buttons.add(InlineKeyboardButton(author, callback_data=f'Review {review[0]}'))
    write_review = InlineKeyboardButton('✍️ Написать отзыв', callback_data='Write Review')
    more_reviews = InlineKeyboardButton('💬 Больше отзывов', url=f'https://t.me/{reviews_channel}')
    back = InlineKeyboardButton('« Назад', callback_data='Main Menu')
        
    buttons \
    .add(write_review) \
    .add(more_reviews) \
    .add(back)
    return buttons


def back_review_main_menu():
    """Отзывы раздел - Назад"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Reviews')
    
    buttons.add(back)
    return buttons
# =============================================== Информационный раздел =============================================== #

def info_menu_user():
    """Информационный раздел"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    exchange = InlineKeyboardButton('🔄 Обмен', callback_data='Exchange')
    balance = InlineKeyboardButton('💰 Баланс', callback_data='Balance')
    my_cabinet = InlineKeyboardButton('🗄 Мой кабинет', callback_data='My Cabinet')
    back = InlineKeyboardButton('« Назад', callback_data='Main Menu')
    
    buttons \
    .add(exchange, balance) \
    .add(my_cabinet) \
    .add(back)
    return buttons


def balance_back_menu_user():
    """Информационный раздел - Баланс"""
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    back = InlineKeyboardButton('« Назад', callback_data='Info')
    
    buttons.add(back)
    return buttons
