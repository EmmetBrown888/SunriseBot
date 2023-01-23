import os
import random
from datetime import datetime

from database.database import get_balance, get_active_currency, get_rate_crypto, get_active_crypto_amount, get_active_ruble_amount, add_active_ruble_amount, get_wallets_admin, get_active_type_card, get_id_mammoth, get_code_word, get_help_text, get_active_wallet_crypto, get_active_commission_crypto, get_active_card_number, get_percent

# service_name = os.environ.get('NAME_SERVICE')
# service_bot_username = os.environ.get('BOT_SERVICE')
# service_chat = os.environ.get('CHAT_SERVICE')
# service_channel = os.environ.get('CHANNEL_SERVICE')
# reviews_channel = os.environ.get('CHANNEL_REVIEWS')
# website_chat = os.environ.get('WEB_SITE_SERVICE')
# operator_support = os.environ.get('OPERATOR_USERNAME')
# min_sum_btc = os.environ.get('MIN_SUM_BTC')
# min_sum_ltc = os.environ.get('MIN_SUM_LTC')
# min_sum_rub = os.environ.get('MIN_SUM_RUB')
# max_sum_btc = os.environ.get('MAX_SUM_BTC')
# max_sum_ltc = os.environ.get('MAX_SUM_LTC')
# max_sum_rub = os.environ.get('MAX_SUM_RUB')
service_name = 'Sunrise'
service_bot_username = 'SunriseBot'
service_chat = 'perehodniksr'
service_channel = 'SunriseCashChanneI'
reviews_channel = 'SunriseCashReviews'
website_chat = 'https://sunrise.cash/'
operator_support = 'Emmett_Browne'
min_sum_btc = 0.00030
min_sum_ltc = 0.14
max_sum_btc = 0.3
max_sum_ltc = 100
min_sum_rub = 2100
max_sum_rub = 327079


async def start_first_text_user():
    return f"""
<b>👋 Добро пожаловать в обменный пункт {service_name}!</b>

<b>🎁 Мы выдали Вам промокод на 30% скидку</b> на первый обмен!

<b>📝 Выплачиваем до 30₽ за отзыв</b>, после успешного обмена!

<b>📢️ Наш канал:</b> @{service_channel}
"""


async def start_second_text_user():
    return f"""
<b>🤖 {service_name}</b> - обменный пункт

<b>🔄 Купить и продать</b> криптовалюту
<b>👛 Личный кошелёк</b> внутри бота.
<b>💸 Деньги за отзывы</b> и не только.
<b>👥 Реферальная</b> система.
🚀 Быстро, удобно, выгодно.
    """

# =============================================== Купить ================================================ #
async def buy_crypto_text_user():
    return """
<b>☑️ Выберите валюту</b> которую Вы хотите <b>купить</b>:
    """

async def enter_amount_crypto_buy(currency):
    symbol = None
    min_amount = None
    max_amount = None
    if currency == 'Bitcoin':
        symbol = 'BTC'
        min_amount = min_sum_btc
        max_amount = max_sum_btc
    elif currency == 'Litecoin':
        symbol = 'LTC'
        min_amount = min_sum_ltc
        max_amount = max_sum_ltc
    return f"""
👛 На какую сумму Вы хотите купить {currency}?

(Напишите сумму: от {min_amount} до {max_amount} {symbol})
    """

async def enter_bitcoin_address_buy_crypto(currency, symbol, amount):
    
    return f"""
Введите <b>{currency}-адрес</b> кошелька, куда Вы хотите отправить: <b>{amount} {symbol}</b>
    """

async def info_about_buy_crypto(user_id):
    currency = await get_active_currency(user_id)
    symbol = None
    rate = None
    if currency == 'Bitcoin':
        symbol = 'BTC'
        rate = await get_rate_crypto(symbol)
    elif currency == 'Litecoin':
        symbol = 'LTC'
        rate = await get_rate_crypto(symbol)
    amount = await get_active_crypto_amount(user_id)
    wallet = await get_active_wallet_crypto(user_id)
    
    amount_commission = await get_active_commission_crypto(user_id)
    sum_buy = int(rate[2] * float(amount)) + amount_commission
    percent_shop = await get_percent()
    sum_buy = sum_buy - (sum_buy / 100 * int(percent_shop))
    return f"""
<b>ℹ️ Информация о Вашем обмене:</b>

↙️ Сумма покупки: <code>{amount}</code> {symbol}
📮 Адрес: <code>{wallet}</code>

<b>☑️ Выберите комиссию на отправку валюты:</b>
<b>🐌 Минимальная</b> - до 120 минут
<b>⚖️ Средняя</b> - до 80 минут
<b>🚀 Высокая</b> - до 60 минут

<b>⏳ Время ориентировочное, может отличаться из-за загрузки сети.</b>

<b>💰 Сумма к оплате</b>: {sum_buy}₽

Выберите нужную комиссию и нажмите кнопку '➡️ Продолжить'
    """


async def info_bid_buy_crypto(user_id):
    currency = await get_active_currency(user_id)
    symbol = None
    rate = None
    if currency == 'Bitcoin':
        symbol = 'BTC'
        rate = await get_rate_crypto(symbol)
    elif currency == 'Litecoin':
        symbol = 'LTC'
        rate = await get_rate_crypto(symbol)
    amount = await get_active_crypto_amount(user_id)
    wallet = await get_active_wallet_crypto(user_id)
    amount_commission = await get_active_commission_crypto(user_id)
    sum_buy = int(rate[2] * float(amount)) + amount_commission
    percent_shop = await get_percent()
    sum_buy = sum_buy - (sum_buy / 100 * int(percent_shop))
    
    return f"""
<b>ℹ️ Информация о заявке</b>

<b>Покупка {currency}</b>: {amount} {symbol}
<b>{currency}-адрес</b>: <code>{wallet}</code>

<b>💵 Сумма перевода</b>: {sum_buy}₽

<b>Выберите способ</b> оплаты:
    """

async def create_bid_buy_crypto(user_id):
    currency = await get_active_currency(user_id)
    symbol = None
    rate = None
    type_card_choose = await get_active_type_card(user_id)
    print('type_card_choose: ', type_card_choose)
    card = await get_wallets_admin(type_card_choose)
    print('card: ', card)
    if currency == 'Bitcoin':
        symbol = 'BTC'
        rate = await get_rate_crypto(symbol)
    elif currency == 'Litecoin':
        symbol = 'LTC'
        rate = await get_rate_crypto(symbol)
    amount = await get_active_crypto_amount(user_id)
    wallet = await get_active_wallet_crypto(user_id)
    amount_commission = await get_active_commission_crypto(user_id)
    sum_buy = int(rate[2] * float(amount)) + amount_commission
    percent_shop = await get_percent()
    sum_buy = sum_buy - (sum_buy / 100 * int(percent_shop))
    num_bid = random.randint(0000000, 9999999)
    return f"""
☑️ Заявка №{num_bid} успешно создана.

<b>Получаете</b>: {amount} {symbol}
<b>{currency}-адрес</b>: <code>{wallet}</code>

<b>💵 Сумма к оплате</b>: <code>{sum_buy}</code>₽
<b>💳 Реквизиты для оплаты</b>:

<code>{card[2]}</code>

<code>⏳ Заявка действительна</code>: 30 минут.

<b>Оплата производится через любые платежные системы</b>: QIWI, перевод с карты на карту, наличные (терминал), Яндекс.Деньги, и другие платежные системы.

ℹ️ После успешного перевода денег по указанным реквизитам нажмите на кнопку «<b>✅Я оплатил(а)</b>» или же Вы можете отменить данную заявку нажав на кнопку «<b>❌Отменить заявку</b>»

<b>⚠️ ВАЖНО</b>! Если Вы оплатите позже 34 минут и курс изменится в большую сторону, то мы будем вынуждены сделать <b>перерасчёт стоимости по актуальному курсу</b>!
    """
# =============================================== Продать =============================================== #
async def sell_crypto_text_user():
    return """
<b>☑️ Выберите валюту</b> которую Вы хотите <b>продать</b>:
    """

async def enter_amount_sell_crypto(currency):
    symbol = None
    min_amount = None
    max_amount = None
    if currency == 'Bitcoin':
        symbol = 'BTC'
        min_amount = min_sum_btc
        max_amount = max_sum_btc
    elif currency == 'Litecoin':
        symbol = 'LTC'
        min_amount = min_sum_ltc
        max_amount = max_sum_ltc
    
    return f"""
На какую сумму Вы хотите продать {currency}?

(Напишите сумму: от <b>{min_amount}</b> до <b>{max_amount}</b> {symbol})

<b>⚠️ Внимание</b>! Выплаты на карты QIWI/ЮMoney не производим, заявка будет отменена.

<b>Если хотите продать сумму больше, свяжитесь с нами</b>: @{operator_support}
    """

async def sell_crypto_wait(currency, symbol, amount):
    return f"""
<b>↗️ Продажа {currency}</b>: {amount} {symbol}

<b>💵 Вы получите после продажи</b>: ⏳₽

ℹ️ Подождите, считаю сумму получения...
    """

async def sell_crypto_get_bid(currency, symbol, amount):
    rate = await get_rate_crypto(symbol)
    sum_sell = int(rate[2] * float(amount))
    
    return f"""
<b>↗️ Продажа {currency}</b>: <code>{amount}</code> {symbol}

<b>💵 Вы получите после продажи</b>: {sum_sell}₽

☑️ Вы согласны продолжить?
    """


async def sell_crypto_add_card(user_id):
    """Ввод Банковской Карты для Выплаты"""
    currency = await get_active_currency(user_id)
    symbol = None
    if currency == 'Bitcoin':
        symbol = 'BTC'
    elif currency == 'Litecoin':
        symbol = 'LTC'
    rate = await get_rate_crypto(symbol)
    amount = await get_active_crypto_amount(user_id)
    sum_sell = int(rate[2] * float(amount))
    return f"""
<b>Продажа {currency}</b>: {amount} {symbol}

<b>💵 Сумма к получению</b>: {sum_sell}₽

<b>💳 Введите номер банковской карты</b>:

<b>⚠️ Внимание</b>! Выплаты на карты QIWI/ЮMoney не производим, заявка будет отменена.
    """


async def sell_crypto_check_bid(user_id, symbol, card):
    rate = await get_rate_crypto(symbol)
    amount = await get_active_crypto_amount(user_id)
    sum_sell = int(rate[2] * float(amount))
    return f"""
☑️ Проверьте правильность введенных Вами данных:

<b>↗️ Сумма продажи</b>: {amount} {symbol}

<b>💳 Реквизиты</b>: {card}
<b>💵 Вы получите после продажи</b>: {sum_sell}₽

<b>Подтверждаете?</b>
    """

async def get_requisites_sell_crypto(user_id):
    currency = await get_active_currency(user_id)
    wallet = await get_wallets_admin(currency)
    symbol = None
    if currency == 'Bitcoin':
        symbol = 'BTC'
    elif currency == 'Litecoin':
        symbol = 'LTC'
    rate = await get_rate_crypto(symbol)
    amount = await get_active_crypto_amount(user_id)
    sum_sell = int(rate[2] * float(amount))
    num_bid = random.randint(0000000, 9999999)
    card_num = await get_active_card_number(user_id)
    return f"""
☑️ Заявка BTC №<code>{num_bid}</code> успешно создана!

Отправьте: <code>{amount}</code> {symbol}

На данный {currency}-адрес:

<code>{wallet[2]}</code>

❗️ Вам нужно перевести ровно: <code>{amount}</code> {symbol} иначе Ваша заявка будет считаться неоплаченной и после чего отменена!

⏳ Заявка действительна: 24 минут.

💵 Сумма к получению: {sum_sell}₽
💳 Ваши реквизиты: {card_num}

ℹ️ После успешной отправки {amount} {symbol} на указанный {currency}-адрес выше, нажмите «✅Я перевел(а)» или же Вы можете отменить данную заявку нажав на кнопку «❌Отменить продажу»

⚠️ ВАЖНО! При отправке {currency} указывайте большую комиссию, если Ваша транзакция получит 1 подтверждение и курс упадёт, то мы будем вынуждены сделать перерасчёт стоимости по актуальному курсу!
    """
# =============================================== Кошелёк =============================================== #
async def wallet_text_user(user_id):
    balance = await get_balance(user_id)
    total_balance = 0
    return f"""
<b>👛 Вы вошли в свой личный кошелёк!</b>

<b>ℹ️ В данном разделе Вы можете:</b> хранить, пополнять, выводить валюту в нужное Вам время.

<b>♻️ Вы можете конвертировать валюты</b> между собой моментально!

<b>💰 Баланс кошелька:</b> ~{total_balance}₽
<b>Рубль:</b> {balance[2]}₽
<b>Bitcoin:</b> {balance[3]} BTC (~0₽)
<b>Litecoin:</b> {balance[4]} LTC (~0₽)

<b>☑️ Выберите кошелёк:</b>  
    """

async def choose_ruble_wallet_text_user(user_id):
    balance = await get_balance(user_id)

    return f"""
<b>👛 Вы вошли в Рубль кошелёк!</b>

<b>💰 Баланс:</b> {balance[2]}₽

🔄️ Данные средства Вы <b>можете потратить, как скидку во время обмена</b> или же вывести удобным Вам способом!

🎰 Так же Вы можете испытать удачу и удвоить или утроить свой баланс в разделе «🎰Лотерея»!

<b>♻️ Вы можете конвертировать эту валюту</b> в любую другую моментально!

Выберите, что Вы хотите сделать:
    """


async def choose_crypto_wallet_text_user(user_id, currency):
    balance = await get_balance(user_id)
    symbol = None
    if currency == 'Bitcoin':
        balance = balance[3]
        symbol = 'BTC'
    elif currency == 'Litecoin':
        balance = balance[4]
        symbol = 'LTC'

    return f"""
<b>👛 Вы вошли в {currency} кошелёк!</b>

<b>💰 Баланс:</b> {balance} {symbol} (~0₽)

<b>Список последних 15 транзакций:</b>

Список пуст!

Выберите, что Вы хотите сделать:
    """


async def converter_currency_text_user():
    return """
<b>♻️ Конвертация валют</b>

ℹ️ В данном разделе Вы можете конвертировать между собой валюты, быстро и моментально!

⛔️ Ваш баланс слишком мал, чтобы совершить конвертацию!

<b>Минимальные суммы:</b>
<b>Рубль:</b> 200.00000000 RUB
<b>Bitcoin:</b> 0.00001000 BTC
<b>Litecoin:</b> 0.00300000 LTC
<b>Tether:</b> 1.00000000 USDT
    """


async def write_voucher_text_user():
    return f"""
<b>🎟 Ввести Ваучер</b>

⛔️ Данный раздел Вам не доступен, т.к. Вы еще не совершили 5 или более обменов!
    """

async def add_balance_text_user(user_id):
    currency = await get_active_currency(user_id)
    print('currency: ', currency)
    min_sum = 0
    max_sum = 0
    symbol = None
    if currency == 'Bitcoin':
        symbol = 'BTC'
        min_sum = min_sum_btc
        max_sum = max_sum_btc
    elif currency == 'Litecoin':
        symbol = 'LTC'
        min_sum = min_sum_ltc
        max_sum = max_sum_ltc
    
    return f"""
👛 На какую сумму Вы хотите пополнить {currency} кошелёк?

(Напишите сумму: от <b>{min_sum}</b> до {max_sum} {symbol})
    """
# =============================================== Рефералка =============================================== #
async def refferal_text_user(user_id):
    return f"""
<b>👤 Рефералка</b>

Приглашайте друзей и получайте % от каждой сделки Вашего друга!

🔄️ Данные средства Вы <b>можете потратить, как скидку во время обмена</b> или же вывести удобным Вам способом!

🎰 Так же Вы можете испытать удачу и удвоить или утроить свой баланс в разделе «🎰Лотерея»!

<b>🔗 Ваша реферальная ссылка:</b>
https://t.me/{service_bot_username}?start=r-{user_id}

<b>💸 Ваш текущий баланс:</b> 0₽
<b>⚖️ Ваш реферальный уровень:</b> 1% из 3%
<b>🆔 для получения:</b> {user_id}

<b>📊 Статистика:</b>
<b>👥 Количество рефералов:</b> 0 шт.
<b>💰 Всего получено от рефералов:</b> 0₽
    """

async def out_money_text_user():
    return f"""
<b>📤 Вывод средств</b>

<b>💰Ваш текущий баланс:</b> 0₽

<b>⚠️ Недостаточно средств! Минимальная сумма вывода:</b> {min_sum_rub}₽
    """

async def send_money_friend_text_user():
    return """
<b>Отправка другу</b>

🚫 Данный раздел Вам не доступен, т.к. Вы еще не совершили 5 или более обменов!🚫
    """

async def count_add_amount(currency, amount, symbol):
    return f"""
<b>Покупка {currency}</b>: {amount} {symbol}

<b>💵 Сумма перевода</b>: ⏳

ℹ️ Подождите, считаю сумму перевода...
"""

async def info_bid(user_id, currency, amount, symbol):
    # Получаем курсы валют
    
    rate = await get_rate_crypto(symbol)
    sum_send = int(rate[2] * float(amount))
    await add_active_ruble_amount(user_id, sum_send)
    return f"""
ℹ️ Информация о заявке

👛 Пополнение {currency} кошелька: {amount} {symbol}

💵 Сумма перевода: {sum_send}₽

Выберите способ оплаты:
"""

async def pay_crypto(user_id):
    bid_num = random.randint(0000000, 9999999)
    currency = await get_active_currency(user_id)
    type_card_choose = await get_active_type_card(user_id)
    wallet = await get_wallets_admin(type_card_choose)
    symbol = None
    if currency == 'Bitcoin':
        symbol = 'BTC'
    elif currency == 'Litecoin':
        symbol = 'LTC'
    amount_crypto = await get_active_crypto_amount(user_id)
    amount_ruble = await get_active_ruble_amount(user_id)
    percent_shop = await get_percent()
    amount_ruble = amount_ruble - (amount_ruble / 100 * int(percent_shop))
    return f"""
☑️ Заявка №{bid_num} успешно создана.

<b>👛 Пополнение {symbol} кошелька:</b> {amount_crypto} {symbol}

<b>💵 Сумма к оплате:</b> {amount_ruble}₽
<b>💳 Реквизиты для оплаты:</b>

<code>{wallet[2]}</code>

<b>⏳ Заявка действительна:</b> 25 минут.

<b>Оплата производится через любые платежные системы:</b> QIWI, перевод с карты на карту, наличные (терминал), Яндекс.Деньги, и другие платежные системы.

ℹ️ После успешного перевода денег по указанным реквизитам нажмите на кнопку <b>«✅Я оплатил(а)»</b> или же Вы можете отменить данную заявку нажав на кнопку <b>«❌Отменить заявку»</b>

<b>⚠️ ВАЖНО!</b> Если Вы оплатите позже 25 минут и курс изменится в большую сторону, то мы будем вынуждены сделать <b>перерасчёт стоимости по актуальному курсу!</b>
    """


async def out_crypto_money(user_id):
    currency = await get_active_currency(user_id)
    balance = await get_balance(user_id)
    min_sum = 0
    symbol = None
    if currency == 'Bitcoin':
        symbol = 'BTC'
        min_sum = min_sum_btc
        balance = balance[3]
    elif currency == 'Litecoin':
        symbol = 'LTC'
        min_sum = min_sum_ltc
        balance = balance[4]
    
    return f"""
Вы не можете вывести {symbol}, т.к Ваш баланс слишком мал!

<b>💰 Ваш баланс:</b> {balance} {symbol}

<b>Минимальная сумма вывода:</b> {min_sum} {symbol}
    """


async def send_crypto_money(user_id):
    currency = await get_active_currency(user_id)
    symbol = None
    if currency == 'Bitcoin':
        symbol = 'BTC'
    elif currency == 'Litecoin':
        symbol = 'LTC'
    return f"""
⚠️ Вы не можете отправить {symbol}, т.к Ваш баланс пуст!
    """


async def create_crypto_voucher_money(user_id):
    currency = await get_active_currency(user_id)
    symbol = None
    if currency == 'Bitcoin':
        symbol = 'BTC'
    elif currency == 'Litecoin':
        symbol = 'LTC'
    return f"""
⚠️ Вы не можете создать {symbol} ваучер, т.к Ваш баланс пуст!
    """


async def create_crypto_link_add_money(user_id):
    currency = await get_active_currency(user_id)
    symbol = None
    if currency == 'Bitcoin':
        symbol = 'BTC'
    elif currency == 'Litecoin':
        symbol = 'LTC'
    return f"""
<b>💸 Создание ссылки на пополнение Вашего {symbol} кошелька</b>

⛔️ Данный раздел Вам не доступен, т.к. Вы еще не совершили 5 или более обменов!
    """
# =============================================== Лотерея =============================================== #
async def lottery_text_user():
    return """
<b>🎰 Лотерея</b>

ℹ️ В данном разделе Вы можете испытать удачу и удвоить или утроить свой баланс из раздела «👤Друзья»!

<b>🍀 Доступно 3 варианта лотереи:</b>
🔳 Вам надо угадать цвет
🎰 Крутить барабан
🎲 Вам надо угадать число от 1 до 6

<b>💸 Ваш текущий баланс:</b> 0₽

❌ Вы не можете сыграть, т.к Ваш баланс меньше 10₽!
    """

# =============================================== Кабинет =============================================== #
async def my_personal_cabinet_text_user(user_id):
    id = await get_id_mammoth(user_id)
    return f"""
<b>🗄 Мой кабинет</b>

<b>⚠️ Установите кодовое слово</b>, чтобы при утере аккаунта перенести Ваши данные на новый!

Вы пока не совершали обменов!

<b>🏆 Всего выиграли:</b> 0₽
<b>🕹 В чат-играх:</b> 0₽

<b>🎫 У Вас есть промокод:</b> NEWUSER{id}

<b>ℹ️ Описание промокода:</b>
🔥 Даёт <b>30% скидку</b> от комиссии на покупку!
    """


async def detailed_statistics_cabinet(user_id):
    id = await get_id_mammoth(user_id)
    return f"""
<b>🗄 Мой кабинет</b>

<b>⚠️ Установите кодовое слово</b>, чтобы при утере аккаунта перенести Ваши данные на новый!

Вы пока не совершали обменов!

<b>🏆 Всего выиграли:</b> 0₽
<b>🎰 В рулетках:</b> 0₽
<b>🍀 В счастливом числе:</b> 0₽

<b>🕹 В чат-играх:</b> 0₽
<b>🎲 Кости:</b> 0₽
<b>🎯 Дартс:</b> 0₽
<b>⚽️ Футбол:</b> 0₽
<b>🏀 Баскетбол:</b> 0₽
<b>🎳 Боулинг:</b> 0₽
<b>🐊 Крокодил:</b> 0₽

<b>🎫 У Вас есть промокод:</b> NEWUSER{id}

<b>ℹ️ Описание промокода:</b>
🔥 Даёт <b>30% скидку</b> от комиссии на покупку!
    """


async def history_exchanges_cabinet():
    return f"""
<b>📋 История обменов</b>

<b>Вы пока не совершали обменов!</b>
    """


async def code_word_cabinet(user_id):
    code_word = await get_code_word(user_id)
    help_text = await get_help_text(user_id)
    if code_word:
        if help_text:
            return f"""
<b>🔐 Кодовое слово</b>

<b>✅ Кодовое слово</b>: установлено

<b>ℹ️ Подсказка</b>: {help_text}

Нажмите, что хотите сделать:
            """
        else:
            return """
<b>🔐 Кодовое слово</b>

<b>✅ Кодовое слово</b>: установлено

Нажмите, что хотите сделать:
            """
    else:
        return f"""
<b>🔐 Кодовое слово</b>

<b>❌ Кодовое слово:</b> не установлено

<b>Нажмите, что хотите сделать:</b>
        """


async def set_code_word_cabinet():
    return """
Введите кодовое слово текстом, которое Вы хотите установить:
    """


async def display_code_word_cabinet(user_id):
    code_word = await get_code_word(user_id)
    return f"""
<b>🔐 Ваше кодовое слово</b>: {code_word}

⚠️ Запишите его, чтобы не забыть! Он не будет нигде больше отображаться!

<b>ℹ️ Хотите установить подсказку для кодового слова</b>, чтобы потом было легче вспомнить?
    """


async def skip_enter_code_word():
    return """
✅ Вы успешно установили кодовое слово!
    """


async def remove_code_word_text():
    return """
Чтобы удалить кодовое слово, введите его:
    """


async def success_remove_code_word_text():
    return """
✅ Вы успешно удалили свое кодовое слово!
    """


async def help_text_remove_code_word_text():
    return """
ℹ️ Введите подсказку текстом, для Вашего кодового слова:
    """


async def success_add_help_text_remove_code_word_text(user_id):
    help_text = await get_help_text(user_id)
    
    return f"""
✅ Вы установили кодовое слово!

ℹ️ Подсказка: {help_text}
    """


def my_personal_add_promocode_word_text():    
    return """
<b>Ввести промокод</b>

🚫 Данный раздел Вам не доступен, т.к. Вы еще не совершили 5 или более обменов!🚫
    """

# =============================================== Розыгрыши =============================================== #
async def practical_jokes_text_user():
    return """
<b>🤑 Добро пожаловать в раздел розыгрышей!</b>

<b>🗓 Расписание розыгрышей</b>:

<b>💲 Воскресенье</b> - Самый везучий

<b>⏲ Результаты в 22:00 по МСК</b>
🏁 После розыгрыша, Вы можете снова принимать участие в конкурсе

<b>ℹ️ Выберите розыгрыш, о котором Вы хотите узнать подробнее:</b>
    """


async def practical_jokes_luckiest_text_user():
    return f"""
<b>🍀 Еженедельный розыгрыш «Самый везучий»</b>

<b>Призы:</b>
🥇 Первое место - 777₽

<b>☑️ Условия розыгрыша:</b>
1️⃣ Совершить в течении недели обмен от 500₽
2️⃣ Быть подписанным на:
✔️ Бот - @{service_bot_username}
✔️ Канал - @{service_channel}
3️⃣ После обмена написать в нашем чате команду: /udacha и выбрать подходящую заявку для регистрации

<b>ℹ️ Дополнительная информация о розыгрыше:</b>

<b>🗓 Розыгрыш проходит каждое воскресенье.</b>

❌ Заявка зарегистрированная для розыгрыша «Суперприз» или «Ручная рулетка» - в этом розыгрыше участвовать не может!

✅ Список участников с их персональным номером участника будет опубликован и закреплен в нашем чате за 30 минут до розыгрыша!

📹 Победители определятся через рандом-сервис под видео пруф, который будет выложен на канале нашего обменного пункта.

<b>🏁 Итоги розыгрыша каждое воскресенье в 22:00 по МСК.</b>

<b>💰 Приз победителям начисляется на баланс</b> в нашем боте.

<b>⚠️ Важно!</b> Участники не выполнившие все условия, к розыгрышу не допускаются!
    """

# ====================================================== Отзывы ======================================================= #
async def reviews_text_user():
    return f"""
<b>📝 Доска отзывов</b>

<b>Последние 10 отзывов</b>:
    """

async def write_review_text_user():
    return f"""
<b>✍️ Написать отзыв</b>

🚫 Данный раздел Вам не доступен, т.к. Вы еще не совершили 1 или более обменов!🚫
    """

async def detail_review_text_user(author, text):
    date_today = datetime.today().strftime("%d-%m-%Y")
    return f"""
📅 Отзыв от {date_today}

👤 Автор: {author}

💬 Текст: {text}
    """
# =============================================== Информационный раздел =============================================== #

async def info_chapter_text_user():
    return f"""
<b>ℹ️ Информационный раздел</b>

В данном разделе, Вы сможете получить ответы на все часто задаваемые вопросы!

🤖 @{service_bot_username} - полностью автоматизирован, все разделы работают в автоматическом режиме.

<b>🔄️ Обмены в 2 стороны</b> - как продаёт, так и скупает.

Выберите раздел, о котором Вы хотите узнать подробнее:
    """


async def balance_text_user():
    return """
<b>💰 Баланс</b>

Все вознаграждения поступают на Ваш баланс в раздел «Рефералка»!

<b>⚙️ Функции баланса:</b>

<b>📮 Скидка во время обмена</b>, а если сумма баланса превышает сумму перевода заявки, то она будет обработана <b>БЕСПЛАТНО</b> и остаток вернётся к Вам на баланс.

<b>💳 Баланс можно вывести следующими способами:</b> EXMO-код, BTC, Банковская карта, QIWI

<b>💸 Как заработать баланс?</b>

<b>👥 Реферальная система</b> - приглашайте друзей и Вы будете получать % от суммы их обменов, какой именно процент Вам начисляется в данный момент, Вы можете узнать в разделе <b>«Рефералка»</b>!

<b>📝 Оставить отзыв</b> - после успешного обмена, Вы можете оставить отзыв нам. За отзыв выплачивается до 30₽!

<b>🎰 За выигрыш в рулетках</b> - средства начислятся в данный раздел.

<b>🕹 За выигрыш в чат-играх</b> - средства начислятся так же в данный раздел.

<b>🥳 Конкурсы</b> в нашем чате
    """


async def exhange_text_user():
    return f"""
<b>🔄 Как совершить обмен?</b>

1️⃣ Для этого Вам нужно в главном меню бота нажать на кнопку «Купить» или «Продать» зависит от того, какой обмен Вы хотите совершить, после чего выбрать нужную Вам валюту и следовать инструкциям бота.

2️⃣ После того, как бот выдаст Вам реквизиты, <b>Вы должны перевести точную сумму, которая написана в заявке.</b> Совершив перевод нажмите кнопку: «✅Я оплатил(а)». Как бот получит уведомление о поступление средств, Ваша заявка сразу же обработается.

<b>⚠️ВАЖНО!</b> Если Вы оплатили меньше, либо больше указанной суммы, то <b>данная заявка будет считаться неоплаченной и отклонена.</b> В данном случае сразу свяжитесь с нашим <b>оператором</b>:
@{operator_support}
    """


async def my_cabinet_text_user():
    return f"""
<b>🗄 Для чего нужен Мой кабинет?</b>

Здесь находится вся необходимая для Вас информация, касаемая вашей статистике обменов. А также - здесь Вы можете хранить и распоряжаться валютой, когда Вам удобно.

<b>👛 Кошелёк</b>. Позволяет Вам пополнять и хранить баланс EXMO или BTC, и в любой момент вывести средства.

<b>📋 История обменов</b>. Здесь Вы всегда можете увидеть свои успешные заявки и всю информацию о них.

<b>🎫 Ввести промокод</b>. Тут Вы можете ввести скидочный промокод, которые мы обычно раздаём в нашем чате
    """