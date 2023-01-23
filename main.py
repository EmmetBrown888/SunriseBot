import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

from tg_bot.keyboards.inline_user import *
from tg_bot.keyboards.reply_user import *
from tg_bot.text.user import *
from tg_bot.utils.validate import validate_form

from tg_bot.text.admin import *
from tg_bot.keyboards.inline_admin import *

from database.database import *

# API_TOKEN = os.environ.get('BOT_TOKEN')
API_TOKEN = '5856981254:AAF0fDNBCKc_kIviU2f6ULk2VvMmiwGVSX4'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class IsAdmin(BoundFilter):
    async def check(self, msg: types.Message):
        # ADMINS = [os.environ.get('ID_ADMINS').split(',')]
        # ADMINS = [5465604654]
        ADMINS = [1144504815]
 
        user = msg.from_user.id
        if user not in ADMINS:
            pass
        return user in ADMINS


# State
class CryptoAdd(StatesGroup):
    amount = State()

class CodeWord(StatesGroup):
    code = State()

class RemoveCodeWord(StatesGroup):
    code = State()

class HelpTextCodeWord(StatesGroup):
    text = State()

class BuyCrypto(StatesGroup):
    amount = State()
    wallet = State()

class SellCrypto(StatesGroup):
    amount = State()

class SellCryptoCard(StatesGroup):
    card = State()

# Admin
class ChangeBitcoinWallet(StatesGroup):
    wallet = State()

class ChangeLitecoinWallet(StatesGroup):
    wallet = State()

class ChangeSberbankCard(StatesGroup):
    card = State()

class ChangeVisaCard(StatesGroup):
    card = State()

class ChangePercentShop(StatesGroup):
    percent = State()

@dp.message_handler(state=CryptoAdd.amount)
async def get_message(message: types.Message, state: CryptoAdd.amount):
    """Получение суммы пополнения"""
    async with state.proxy() as data:
        data['message'] = message.text

    currency = await get_active_currency(message.from_user.id)
    res_valid = await validate_form('amount_crypto', message, currency)
    if res_valid:
        await state.finish()
        symbol = None
        if currency == 'Bitcoin':
            symbol = 'BTC'
        elif currency == 'Litecoin':
            symbol = 'LTC'
        await message.answer(await count_add_amount(currency, data['message'], symbol))
        # Добавляем значение в базу данных
        await add_active_crypto_amount(message.from_user.id, float(data['message']))
        await message.answer(await info_bid(message.from_user.id, currency, data['message'], symbol), reply_markup=method_pay_buy_crypto())


@dp.message_handler(state=CodeWord.code)
async def get_code_word(message: types.Message, state: CodeWord.code):
    """Получение Кодового Слова"""
    async with state.proxy() as data:
        data['message'] = message.text

    await state.finish()
    # Добавления Кодового Слова в Базу Данных
    await add_code_word(message.from_user.id, data['message'])
    await message.answer(await display_code_word_cabinet(message.from_user.id), reply_markup=display_code_menu_user(), parse_mode='HTML')


@dp.message_handler(state=RemoveCodeWord.code)
async def remove_code_word(message: types.Message, state: RemoveCodeWord.code):
    """Удаление Кодового Слова"""
    async with state.proxy() as data:
        data['message'] = message.text
    
    valid_code_word = await check_exist_code_word(message.from_user.id, data['message'])
    if valid_code_word:
        await state.finish()
        # Удаляем из базы данных Кодовое Слово
        await delete_code_word(message.from_user.id)
        await message.answer(await success_remove_code_word_text(), reply_markup=skip_code_menu_user(), parse_mode='HTML')
    else:
        await message.answer('❌ Вы ввели неверное кодовое слово!', reply_markup=remove_code_menu_user())


@dp.message_handler(state=HelpTextCodeWord.text)
async def add_text_code(message: types.Message, state: HelpTextCodeWord.text):
    """Добавление Подсказки к Кодовому Слову"""
    async with state.proxy() as data:
        data['message'] = message.text
    
    await state.finish()
    # Добавляем Подсказку в базу данных
    await add_help_text_word(message.from_user.id, data['message'])
    await message.answer(await success_add_help_text_remove_code_word_text(message.from_user.id), reply_markup=skip_code_menu_user(), parse_mode='HTML')


@dp.message_handler(state=BuyCrypto.amount)
async def buy_crypto_text_amount(message: types.Message, state: BuyCrypto.amount):
    """Покупка Криптовалюты - Ввод суммы"""
    async with state.proxy() as data:
        data['amount'] = message.text
    
    currency = await get_active_currency(message.from_user.id)
    res_valid = await validate_form('amount_crypto', message, currency)
    if res_valid:
        await BuyCrypto.next()
        symbol = None
        if currency == 'Bitcoin':
            symbol = 'BTC'
        elif currency == 'Litecoin':
            symbol = 'LTC'
        await message.answer(await count_add_amount(currency, data['amount'], symbol), parse_mode='HTML')
        # Добавляем значение в базу данных
        await add_active_crypto_amount(message.from_user.id, float(data['amount']))
        await message.answer(await enter_bitcoin_address_buy_crypto(currency, symbol, data['amount']), reply_markup=cancel_enter_crypto_wallet_menu_user(), parse_mode='HTML')


@dp.message_handler(state=BuyCrypto.wallet)
async def buy_crypto_text_wallet(message: types.Message, state: BuyCrypto.wallet):
    """Покупка Криптовалюты - Ввод Кошелька"""
    async with state.proxy() as data:
        data['wallet'] = message.text
    print('Ввод Кошелька')
    currency = await get_active_currency(message.from_user.id)
    print('currency - Ввод Кошелька: ', currency)
    res_valid = None
    if currency == 'Bitcoin':
        res_valid = await validate_form('bitcoin_wallet', message, currency)
    elif currency == 'Litecoin':
        res_valid = await validate_form('litecoin_wallet', message, currency)
    if res_valid:
        await state.finish()
        symbol = None
        if currency == 'Bitcoin':
            symbol = 'BTC'
        elif currency == 'Litecoin':
            symbol = 'LTC'
        await message.answer(await count_add_amount(currency, data['wallet'], symbol), parse_mode='HTML')
        # Добавляем Кошелька в базу данных
        await add_wallet_crypto(message.from_user.id, data['wallet'])
        await message.answer(await info_about_buy_crypto(message.from_user.id), reply_markup=info_detail_min_commission_crypto_buy_menu_user(), parse_mode='HTML')


@dp.message_handler(state=SellCrypto.amount)
async def sell_crypto_text_amount(message: types.Message, state: SellCrypto.amount):
    """Продажа Криптовалюты - Ввод суммы"""
    async with state.proxy() as data:
        data['amount'] = message.text
    
    currency = await get_active_currency(message.from_user.id)
    res_valid = await validate_form('sell_amount_crypto', message, currency)
    if res_valid:
        await state.finish()
        symbol = None
        if currency == 'Bitcoin':
            symbol = 'BTC'
        elif currency == 'Litecoin':
            symbol = 'LTC'
        await message.answer(await sell_crypto_wait(currency, symbol, data['amount']), parse_mode='HTML')
        # Добавляем значение в базу данных
        await add_active_crypto_amount(message.from_user.id, float(data['amount']))
        await message.answer(await sell_crypto_get_bid(currency, symbol, data['amount']), reply_markup=sell_continue_menu_user(), parse_mode='HTML')


@dp.message_handler(state=SellCryptoCard.card)
async def sell_crypto_card_text(message: types.Message, state: SellCryptoCard.card):
    """Продажа Криптовалюты - Ввод карты"""
    async with state.proxy() as data:
        data['card'] = message.text
    
    currency = await get_active_currency(message.from_user.id)
    res_valid = await validate_form('card_number', message, currency)
    if res_valid:
        await state.finish()
        symbol = None
        if currency == 'Bitcoin':
            symbol = 'BTC'
        elif currency == 'Litecoin':
            symbol = 'LTC'
        # Добавляем значение в базу данных
        await add_active_card_number(message.from_user.id, data['card'])
        await message.answer(await sell_crypto_check_bid(message.from_user.id, symbol, data['card']), reply_markup=sell_continue_menu_user_2(), parse_mode='HTML')

# Admin
@dp.message_handler(state=ChangeBitcoinWallet.wallet)
async def change_bitcoin_wallet_text(message: types.Message, state: ChangeBitcoinWallet.wallet):
    """Изменение Bitcoin Кошелька - Админ"""
    async with state.proxy() as data:
        data['wallet'] = message.text
    
    res_valid = await validate_form('bitcoin_wallet', message)
    if res_valid:
        await state.finish()
        # Изменяем Кошелек в базе данных
        await change_wallet_admin('bitcoin', data['wallet'])
        await message.answer(await success_change_wallet('Bitcoin'), reply_markup=back_wallets_menu_admin(), parse_mode='HTML')

@dp.message_handler(state=ChangeLitecoinWallet.wallet)
async def change_litecoin_wallet_text(message: types.Message, state: ChangeLitecoinWallet.wallet):
    """Изменение Litecoin Кошелька - Админ"""
    async with state.proxy() as data:
        data['wallet'] = message.text
    
    res_valid = await validate_form('litecoin_wallet', message)
    if res_valid:
        await state.finish()
        # Изменяем Кошелек в базе данных
        await change_wallet_admin('litecoin', data['wallet'])
        await message.answer(await success_change_wallet('Litecoin'), reply_markup=back_wallets_menu_admin(), parse_mode='HTML')

@dp.message_handler(state=ChangeSberbankCard.card)
async def change_sberbank_wallet_text(message: types.Message, state: ChangeSberbankCard.card):
    """Изменение Sberbank Кошелька - Админ"""
    async with state.proxy() as data:
        data['card'] = message.text
    
    res_valid = await validate_form('card_number', message)
    if res_valid:
        await state.finish()
        # Изменяем Номер Карты в базе данных
        await change_wallet_admin('sberbank', data['card'])
        await message.answer(await success_change_wallet('Sberbank'), reply_markup=back_wallets_menu_admin(), parse_mode='HTML')

@dp.message_handler(state=ChangeVisaCard.card)
async def change_visa_wallet_text(message: types.Message, state: ChangeVisaCard.card):
    """Изменение Visa Кошелька - Админ"""
    async with state.proxy() as data:
        data['card'] = message.text
    
    res_valid = await validate_form('card_number', message)
    if res_valid:
        await state.finish()
        # Изменяем Номер Карты в базе данных
        await change_wallet_admin('visa', data['card'])
        await message.answer(await success_change_wallet('Visa'), reply_markup=back_wallets_menu_admin(), parse_mode='HTML')

@dp.message_handler(state=ChangePercentShop.percent)
async def change_percent_bot_text(message: types.Message, state: ChangePercentShop.percent):
    """Изменение Процента Бота - Админ"""
    async with state.proxy() as data:
        data['percent'] = message.text
    
    res_valid = await validate_form('percent', message)
    if res_valid:
        await state.finish()
        # Изменяем Процент Бота в базе данных
        await change_percent(data['percent'])
        await message.answer(await success_change_percent_admin(), reply_markup=back_settings_menu_admin(), parse_mode='HTML')


# Cancel Handlers
@dp.callback_query_handler(text='Cancel', state=CryptoAdd.amount)
async def cancel_crypto_add_handler(query: types.CallbackQuery, state: CryptoAdd.amount):
    """Отмена пополнения"""
    await state.finish()
    await delete_before_message(query)
    await query.message.answer(await wallet_text_user(query.message.chat.id), reply_markup=wallet_menu_user(), parse_mode='HTML') 

@dp.callback_query_handler(text='Cancel Code Word', state=CodeWord.code)
async def cancel_code_word_add_handler(query: types.CallbackQuery, state: CodeWord.code):
    """Отмена Ввода Кодового Слова"""
    mammoth_id = query.message.chat.id
    await state.finish()
    await delete_before_message(query)
    await query.message.answer(await code_word_cabinet(mammoth_id), reply_markup=await code_word_menu_user(mammoth_id), parse_mode='HTML')


@dp.callback_query_handler(text='Remove Code Word', state=RemoveCodeWord.code)
async def remove_code_word_add_handler(query: types.CallbackQuery, state: RemoveCodeWord.code):
    """Удаление Кодового Слова"""
    mammoth_id = query.message.chat.id
    await state.finish()
    await delete_before_message(query)
    # Удаляем Текст Подсказку
    help_text = await get_help_text(mammoth_id)
    if help_text:
        await delete_help_text(mammoth_id)
    
    await query.message.answer(await code_word_cabinet(mammoth_id), reply_markup=await code_word_menu_user(mammoth_id), parse_mode='HTML')


@dp.callback_query_handler(text='Cancel Add Help Text Word', state=HelpTextCodeWord.text)
async def cancel_help_text_add_handler(query: types.CallbackQuery, state: HelpTextCodeWord.text):
    """Отмена Добавления Подсказки"""
    mammoth_id = query.message.chat.id
    await state.finish()
    await delete_before_message(query)
    await query.message.answer(await code_word_cabinet(mammoth_id), reply_markup=await code_word_menu_user(mammoth_id), parse_mode='HTML')

@dp.callback_query_handler(text='Cancel Buy CryptoCurrency', state=BuyCrypto.amount)
async def cancel_buy_crypto_handler(query: types.CallbackQuery, state: BuyCrypto.amount):
    """Отмена Ввода Суммы Покупки Криптовалюты"""
    await state.finish()
    await delete_before_message(query)
    await query.message.answer(await buy_crypto_text_user(), reply_markup=buy_crypto_menu_user(), parse_mode='HTML')

@dp.callback_query_handler(text='Cancel Enter Crypto Wallet', state=BuyCrypto.wallet)
async def cancel_enter_crypto_handler(query: types.CallbackQuery, state: BuyCrypto.wallet):
    """Отмена Ввода Крипто Кошелька"""
    await state.finish()
    await delete_before_message(query)
    await query.message.answer(await buy_crypto_text_user(), reply_markup=buy_crypto_menu_user(), parse_mode='HTML')

@dp.callback_query_handler(text='Cancel Sell CryptoCurrency', state=SellCrypto.amount)
async def cancel_enter_amount_sell_handler(query: types.CallbackQuery, state: SellCrypto.amount):
    """Отмена Ввода Суммы Продажи Криптовалюты"""
    print('CANCEL SELL CRYPTOCURRENCY')
    await state.finish()
    await delete_before_message(query)
    await query.message.answer(await sell_crypto_text_user(), reply_markup=sell_crypto_menu_user(), parse_mode='HTML')

@dp.callback_query_handler(text='Cancel Sell CryptoCurrency Enter Card', state=SellCryptoCard.card)
async def cancel_enter_card_sell_handler(query: types.CallbackQuery, state: SellCryptoCard.card):
    """Отмена Ввода Реквизитов Карты при Продажи Криптовалюты"""
    print('CANCEL SELL CRYPTOCURRENCY ADD CARD')
    await state.finish()
    await delete_before_message(query)
    await query.message.answer(await sell_crypto_text_user(), reply_markup=sell_crypto_menu_user(), parse_mode='HTML')

# Admin
@dp.callback_query_handler(text='Cancel Change Bitcoin wallet', state=ChangeBitcoinWallet.wallet)
async def cancel_change_btc_handler(query: types.CallbackQuery, state: ChangeBitcoinWallet.wallet):
    """Отмена Изменения Bitcoin Кошелька"""
    print('CANCEL CHANGE BITCOIN WALLET')
    await state.finish()
    await delete_before_message(query)
    await query.message.answer(await my_wallet_admin_menu(), reply_markup=my_wallets_menu_admin(), parse_mode='HTML')

@dp.callback_query_handler(text='Cancel Change Litecoin wallet', state=ChangeLitecoinWallet.wallet)
async def cancel_change_ltc_handler(query: types.CallbackQuery, state: ChangeLitecoinWallet.wallet):
    """Отмена Изменения Litecoin Кошелька"""
    print('CANCEL CHANGE LITECOIN WALLET')
    await state.finish()
    await delete_before_message(query)
    await query.message.answer(await my_wallet_admin_menu(), reply_markup=my_wallets_menu_admin(), parse_mode='HTML')

@dp.callback_query_handler(text='Cancel Change Sberbank wallet', state=ChangeSberbankCard.card)
async def cancel_change_sber_handler(query: types.CallbackQuery, state: ChangeSberbankCard.card):
    """Отмена Изменения Sberbank Кошелька"""
    print('CANCEL CHANGE SBERBANK WALLET')
    await state.finish()
    await delete_before_message(query)
    await query.message.answer(await my_wallet_admin_menu(), reply_markup=my_wallets_menu_admin(), parse_mode='HTML')

@dp.callback_query_handler(text='Cancel Change Visa wallet', state=ChangeVisaCard.card)
async def cancel_change_visa_handler(query: types.CallbackQuery, state: ChangeVisaCard.card):
    """Отмена Изменения Visa Кошелька"""
    print('CANCEL CHANGE VISA WALLET')
    await state.finish()
    await delete_before_message(query)
    await query.message.answer(await my_wallet_admin_menu(), reply_markup=my_wallets_menu_admin(), parse_mode='HTML')

@dp.callback_query_handler(text='Cancel Change Percent Admin', state=ChangePercentShop.percent)
async def cancel_change_percent_handler(query: types.CallbackQuery, state: ChangePercentShop.percent):
    """Отмена Изменения Процента Бота"""
    print('CANCEL CHANGE PERCENT BOT')
    await state.finish()
    await delete_before_message(query)
    await query.message.answer(await settings_admin_text(), reply_markup=settings_menu_admin(), parse_mode='HTML')

# Handlers
async def delete_before_message(query: types.CallbackQuery):
    await bot.delete_message(query.message.chat.id, query.message.message_id)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """Команда /start"""
    # Добавление Мамонта в БД
    await add_mammoth(message.from_user.id, message.from_user.username)
    await message.answer(await start_first_text_user(), parse_mode='HTML')
    await message.answer(await start_second_text_user(), reply_markup=main_menu_user(), parse_mode='HTML')


# Админка
@dp.message_handler(IsAdmin(), commands=['admin'])
async def send_welcome(message: types.Message):
    """Команда /admin"""
    await message.answer(await start_text_admin(), reply_markup=start_menu_admin(), parse_mode='HTML')


@dp.message_handler()
async def commands_echo_user(message: types.Message):
    pass

# =============================================== Купить ================================================ #
@dp.callback_query_handler(text='Buy')
async def buy_crypto_handler(query: types.CallbackQuery):
    """Купить раздел"""
    await delete_before_message(query)
    await query.message.answer(await buy_crypto_text_user(), reply_markup=buy_crypto_menu_user(), parse_mode='HTML')


@dp.callback_query_handler(text=['Buy Bitcoin', 'Buy Litecoin'])
async def choose_buy_crypto_handler(query: types.CallbackQuery):
    """Купить раздел - Выбрать Валюту"""
    currency = query.data.split(' ')[1].strip()
    mammoth_id = query.message.chat.id
    await add_active_currency(mammoth_id, currency)
    await delete_before_message(query)
    await BuyCrypto.amount.set()
    await query.message.answer(await enter_amount_crypto_buy(currency), reply_markup=cancel_enter_buy_crypto_menu_user(), parse_mode='HTML')

@dp.callback_query_handler(text='Min Commission')
async def buy_crypto_min_comm_handler(query: types.CallbackQuery):
    """Купить раздел - Минимальная Коммиссия"""
    mammoth_id = query.message.chat.id
    # Добавляем коммиссию
    await add_active_commission_crypto(mammoth_id, 0)
    await delete_before_message(query)
    await query.message.answer(await info_about_buy_crypto(mammoth_id), reply_markup=info_detail_min_commission_crypto_buy_menu_user(), parse_mode='HTML')

@dp.callback_query_handler(text='Average Commission')
async def buy_crypto_average_comm_handler(query: types.CallbackQuery):
    """Купить раздел - Средняя Коммиссия"""
    mammoth_id = query.message.chat.id
    # Добавляем коммиссию
    await add_active_commission_crypto(mammoth_id, 23)
    await delete_before_message(query)
    await query.message.answer(await info_about_buy_crypto(mammoth_id), reply_markup=await info_detail_average_commission_crypto_buy_menu_user(mammoth_id), parse_mode='HTML')

@dp.callback_query_handler(text='High Commission')
async def buy_crypto_high_comm_handler(query: types.CallbackQuery):
    """Купить раздел - Высокая Коммиссия"""
    mammoth_id = query.message.chat.id
    # Добавляем коммиссию
    await add_active_commission_crypto(mammoth_id, 75)
    await delete_before_message(query)
    await query.message.answer(await info_about_buy_crypto(mammoth_id), reply_markup=await info_detail_high_commission_crypto_buy_menu_user(mammoth_id), parse_mode='HTML')

@dp.callback_query_handler(text='Continue Commission')
async def buy_crypto_continue_handler(query: types.CallbackQuery):
    """Купить раздел - Продолжить"""
    mammoth_id = query.message.chat.id
    await delete_before_message(query)
    await query.message.answer(await info_bid_buy_crypto(mammoth_id), reply_markup=continue_crypto_buy_menu_user(), parse_mode='HTML')

@dp.callback_query_handler(text=['Main Buy Crypto Sberbank', 'Main Buy Crypto Visa'])
async def get_requisites_buy_crypto(query: types.CallbackQuery):
    """Купить раздел - Получение реквизитов"""
    type_card = query.data.split(' ')[-1].strip()
    mammoth_id = query.message.chat.id
    await add_active_type_card(mammoth_id, type_card)
    await delete_before_message(query)
    await query.message.answer(await create_bid_buy_crypto(mammoth_id), reply_markup=create_bid_crypto(), parse_mode='HTML')

# =============================================== Продать ================================================ #
@dp.callback_query_handler(text='Sell')
async def sell_crypto_handler(query: types.CallbackQuery):
    """Продать раздел"""
    await delete_before_message(query)
    await query.message.answer(await sell_crypto_text_user(), reply_markup=sell_crypto_menu_user(), parse_mode='HTML')


@dp.callback_query_handler(text=['Sell Bitcoin', 'Sell Litecoin'])
async def sell_crypto_choose_handler(query: types.CallbackQuery):
    """Продать раздел - Продать Валюту"""
    currency = query.data.split(' ')[1].strip()
    print('currency: ', currency)
    mammoth_id = query.message.chat.id
    await add_active_currency(mammoth_id, currency)
    await delete_before_message(query)
    await SellCrypto.amount.set()
    await query.message.answer(await enter_amount_sell_crypto(currency), reply_markup=sell_enter_amount_menu_user(), parse_mode='HTML')

@dp.callback_query_handler(text='Continue Sell CryptoCurrency')
async def sell_continue_crypto_handler(query: types.CallbackQuery):
    """Продать раздел - Продать Валюту"""
    mammoth_id = query.message.chat.id
    await delete_before_message(query)
    await SellCryptoCard.card.set()
    await query.message.answer(await sell_crypto_add_card(mammoth_id), reply_markup=sell_enter_card_menu_user(), parse_mode='HTML')

@dp.callback_query_handler(text='Continue Sell CryptoCurrency 2')
async def sell_continue_crypto_2_handler(query: types.CallbackQuery):
    """Продать раздел -  Продолжить для получения реквизитов"""
    mammoth_id = query.message.chat.id
    await delete_before_message(query)
    await query.message.answer(await get_requisites_sell_crypto(mammoth_id), reply_markup=create_bid_crypto(), parse_mode='HTML')

# =============================================== Кошелёк =============================================== #
@dp.callback_query_handler(text='Wallet')
async def wallet_handler(query: types.CallbackQuery):
    """Кошелёк раздел"""
    await delete_before_message(query)
    await query.message.answer(await wallet_text_user(query.message.chat.id), reply_markup=wallet_menu_user(), parse_mode='HTML')


@dp.callback_query_handler(text=['Choose Ruble Wallet', 'Choose Bitcoin Wallet', 'Choose Litecoin Wallet'])
async def choose_ruble_wallet_handler(query: types.CallbackQuery):
    """Выбраный Bitcoin Кошелёк раздел"""
    currency = query.data.split(' ')[1].strip()
    mammoth_id = query.message.chat.id
    # Добавляем в базу Данных Выбранную валюту
    await add_active_currency(mammoth_id, currency)
    await delete_before_message(query)
    if currency == 'Ruble':
        await query.message.answer(await choose_ruble_wallet_text_user(query.message.chat.id), reply_markup=choose_ruble_wallet_menu_user(), parse_mode='HTML')
    else:
        await query.message.answer(await choose_crypto_wallet_text_user(mammoth_id, currency), reply_markup=choose_crypto_wallet_menu_user(), parse_mode='HTML')


@dp.callback_query_handler(text='Converter Currency')
async def converter_currency_handler(query: types.CallbackQuery):
    """Конвертер Валют"""
    await delete_before_message(query)
    await query.message.answer(await converter_currency_text_user(), reply_markup=converter_currency(), parse_mode='HTML')


@dp.callback_query_handler(text='Write Voucher')
async def write_voucher_handler(query: types.CallbackQuery):
    """Конвертер Ввести ваучер"""
    await delete_before_message(query)
    await query.message.answer(await write_voucher_text_user(), reply_markup=write_voucher_currency(), parse_mode='HTML')


# Пополнить баланс
@dp.callback_query_handler(text='Add Balance')
async def add_balance_handler(query: types.CallbackQuery):
    """Пополнение баланса Крипто"""
    mammoth_id = query.message.chat.id
    await delete_before_message(query)
    await CryptoAdd.amount.set()
    await query.message.answer(await add_balance_text_user(mammoth_id), reply_markup=add_balance_currency(), parse_mode='HTML')


# Пополнить баланс
@dp.callback_query_handler(text='Add Balance')
async def add_balance_handler(query: types.CallbackQuery):
    """Пополнение баланса Крипто"""
    mammoth_id = query.message.chat.id
    await delete_before_message(query)
    await CryptoAdd.amount.set()
    await query.message.answer(await add_balance_text_user(mammoth_id), reply_markup=add_balance_currency(), parse_mode='HTML')

# Сбербанк
@dp.callback_query_handler(text=['Buy Crypto Sberbank', 'Buy Crypto Visa'])
async def buy_crypto_handler(query: types.CallbackQuery):
    """Пополнение баланса через Крипту"""
    type_card = query.data.split(' ')[-1].strip()
    mammoth_id = query.message.chat.id
    await add_active_type_card(mammoth_id, type_card)
    mammoth_id = query.message.chat.id
    await query.message.answer(await pay_crypto(mammoth_id), reply_markup=create_bid_crypto(), parse_mode='HTML')


@dp.callback_query_handler(text='Out to Card')
async def out_crypto_handler(query: types.CallbackQuery):
    """Вывести крипту на карту"""
    mammoth_id = query.message.chat.id
    await query.message.answer(await out_crypto_money(mammoth_id), reply_markup=converter_currency(), parse_mode='HTML')


@dp.callback_query_handler(text='Send')
async def send_crypto_handler(query: types.CallbackQuery):
    """Отправить крипту"""
    mammoth_id = query.message.chat.id
    await query.message.answer(await send_crypto_money(mammoth_id), reply_markup=converter_currency(), parse_mode='HTML')


@dp.callback_query_handler(text='Create Voucher')
async def send_crypto_handler(query: types.CallbackQuery):
    """Создать Ваучер крипты"""
    mammoth_id = query.message.chat.id
    await query.message.answer(await create_crypto_voucher_money(mammoth_id), reply_markup=converter_currency(), parse_mode='HTML')


@dp.callback_query_handler(text='Link to add')
async def create_link_add_crypto_handler(query: types.CallbackQuery):
    """Создать Ссылку для пополнения крипты"""
    mammoth_id = query.message.chat.id
    await query.message.answer(await create_crypto_link_add_money(mammoth_id), reply_markup=create_link_voucher_currency_keyboard(), parse_mode='HTML')


@dp.callback_query_handler(text='Out money Ruble')
async def out_money_handler(query: types.CallbackQuery):
    """Рефералка раздел - Вывод средств"""
    await delete_before_message(query)
    await query.message.answer(await out_money_text_user(), reply_markup=converter_currency(), parse_mode='HTML')


@dp.callback_query_handler(text='Send Ruble To Friend')
async def send_money_friend_handler(query: types.CallbackQuery):
    """Рефералка раздел - Отправка Другу"""
    await delete_before_message(query)
    await query.message.answer(await send_money_friend_text_user(), reply_markup=converter_currency(), parse_mode='HTML')
# =============================================== Рефералка =============================================== #
@dp.callback_query_handler(text='Refferal')
async def refferal_handler(query: types.CallbackQuery):
    """Рефералка раздел"""
    await delete_before_message(query)
    await query.message.answer(await refferal_text_user(query.message.chat.id), reply_markup=refferal_menu_user(), parse_mode='HTML')


@dp.callback_query_handler(text='Out money')
async def out_money_handler(query: types.CallbackQuery):
    """Рефералка раздел - Вывод средств"""
    await delete_before_message(query)
    await query.message.answer(await out_money_text_user(), reply_markup=refferal_back_menu_user(), parse_mode='HTML')


@dp.callback_query_handler(text='Send Money To Friend')
async def send_money_friend_handler(query: types.CallbackQuery):
    """Рефералка раздел - Отправка Другу"""
    await delete_before_message(query)
    await query.message.answer(await send_money_friend_text_user(), reply_markup=refferal_back_menu_user(), parse_mode='HTML')



# =============================================== Лотерея =============================================== #
@dp.callback_query_handler(text='Lottery')
async def lottery_handler(query: types.CallbackQuery):
    """Лотерея раздел"""
    await delete_before_message(query)
    await query.message.answer(await lottery_text_user(), reply_markup=lottery_menu_user(), parse_mode='HTML')


# =============================================== Мой Кабинет =============================================== #
@dp.callback_query_handler(text='My Personal Cabinet')
async def my_personal_cabinet_handler(query: types.CallbackQuery):
    """Мой Персональный Кабинет раздел"""
    mammoth_id = query.message.chat.id
    await delete_before_message(query)
    await query.message.answer(await my_personal_cabinet_text_user(mammoth_id), reply_markup=my_personal_cabinet_menu_user(), parse_mode='HTML')


@dp.callback_query_handler(text='Detailed statistics')
async def my_detailed_stats_handler(query: types.CallbackQuery):
    """Кабинет раздел - Детальная Статистика"""
    mammoth_id = query.message.chat.id
    await delete_before_message(query)
    await query.message.answer(await detailed_statistics_cabinet(mammoth_id), reply_markup=detail_stats_cabinet_menu_user(), parse_mode='HTML')


@dp.callback_query_handler(text='Brief statistics')
async def my_brief_stats_handler(query: types.CallbackQuery):
    """Кабинет раздел - Краткая Статистика"""
    mammoth_id = query.message.chat.id
    await delete_before_message(query)
    await query.message.answer(await my_personal_cabinet_text_user(mammoth_id), reply_markup=my_personal_cabinet_menu_user(), parse_mode='HTML')


@dp.callback_query_handler(text='History Exchanges')
async def my_history_exchanges_handler(query: types.CallbackQuery):
    """Кабинет раздел - История Обменов"""
    await delete_before_message(query)
    await query.message.answer(await history_exchanges_cabinet(), reply_markup=history_exchanges_menu_user(), parse_mode='HTML')


@dp.callback_query_handler(text='Code Word')
async def my_code_word_handler(query: types.CallbackQuery):
    """Кабинет раздел - Кодовое слово"""
    mammoth_id = query.message.chat.id
    await delete_before_message(query)
    await query.message.answer(await code_word_cabinet(mammoth_id), reply_markup=await code_word_menu_user(mammoth_id), parse_mode='HTML')


@dp.callback_query_handler(text='Set Code Word')
async def my_code_word_set_handler(query: types.CallbackQuery):
    """Кабинет раздел - Установить Кодовое слово"""
    await delete_before_message(query)
    await CodeWord.code.set()
    await query.message.answer(await set_code_word_cabinet(), reply_markup=cancel_set_code_menu_user(), parse_mode='HTML')


@dp.callback_query_handler(text='Skip Code Word')
async def skip_code_word_set_handler(query: types.CallbackQuery):
    """Кабинет раздел - Пропустить Кодовое слово"""
    mammoth_id = query.message.chat.id
    await delete_before_message(query)
    await delete_help_text(mammoth_id)
    await query.message.answer(await skip_enter_code_word(), reply_markup=skip_code_menu_user(), parse_mode='HTML')


@dp.callback_query_handler(text='Code Word Dont Set')
async def my_cancel_code_word_handler(query: types.CallbackQuery):
    """Кабинет раздел - Кодовое слово"""
    mammoth_id = query.message.chat.id
    await delete_before_message(query)
    # Удаляем из базы данных Кодовое Слово
    await delete_code_word(mammoth_id)
    await query.message.answer(await code_word_cabinet(mammoth_id), reply_markup=await code_word_menu_user(mammoth_id), parse_mode='HTML')


@dp.callback_query_handler(text='Delete Code Word')
async def my_remove_code_word_handler(query: types.CallbackQuery):
    """Кабинет раздел - Удалить Кодовое слово"""
    await delete_before_message(query)
    await RemoveCodeWord.code.set()
    await query.message.answer(await remove_code_word_text(), reply_markup=remove_code_menu_user(), parse_mode='HTML')


@dp.callback_query_handler(text='Approve Code Word')
async def add_text_code_word_handler(query: types.CallbackQuery):
    """Кабинет раздел - Удалить Кодовое слово"""
    await delete_before_message(query)
    await HelpTextCodeWord.text.set()
    await query.message.answer(await help_text_remove_code_word_text(), reply_markup=cancel_add_code_menu_user(), parse_mode='HTML')


@dp.callback_query_handler(text='Enter promo code')
async def enter_promo_code_word_handler(query: types.CallbackQuery):
    """Кабинет раздел - Ввести промокод"""
    await delete_before_message(query)
    await query.message.answer(my_personal_add_promocode_word_text(), reply_markup=history_exchanges_menu_user(), parse_mode='HTML')
# =============================================== Розыгрыши раздел =============================================== #
@dp.callback_query_handler(text='Practical jokes')
async def practical_jokes_handler(query: types.CallbackQuery):
    """Розыгрыши раздел"""
    await delete_before_message(query)
    await query.message.answer(await practical_jokes_text_user(), reply_markup=practical_jokes_menu_user(), parse_mode='HTML')

# Самый везучий
@dp.callback_query_handler(text='The luckiest')
async def practical_jokes_luckiest_handler(query: types.CallbackQuery):
    """Розыгрыши раздел - Самый везучий"""
    await delete_before_message(query)
    await query.message.answer(await practical_jokes_luckiest_text_user(), reply_markup=practical_jokes_back_menu_user(), parse_mode='HTML')

# ====================================================== Отзывы ======================================================= #
@dp.callback_query_handler(text='Reviews')
async def reviews_handler(query: types.CallbackQuery):
    """Отзывы раздел"""
    await delete_before_message(query)
    await query.message.answer(await reviews_text_user(), reply_markup=await reviews_menu_user(), parse_mode='HTML')


@dp.callback_query_handler(text=['Review 1', 'Review 2', 'Review 3', 'Review 4', 'Review 5', 'Review 6', 'Review 7', 'Review 8', 'Review 9', 'Review 10'])
async def show_review_handler(query: types.CallbackQuery):
    """Отзывы раздел - Посмотреть отзыв"""
    num_review = query.data.split(' ')[1].strip()
    review = await get_review(num_review)
    await delete_before_message(query)
    await query.message.answer(await detail_review_text_user(review[1], review[2]), reply_markup=back_review_main_menu(), parse_mode='HTML')


@dp.callback_query_handler(text='Write Review')
async def write_review_handler(query: types.CallbackQuery):
    """Отзывы раздел - Написать отзыв"""
    await delete_before_message(query)
    await query.message.answer(await write_review_text_user(), reply_markup=back_review_main_menu(), parse_mode='HTML')

# =============================================== Информационный раздел =============================================== #
@dp.callback_query_handler(text='Info')
async def info_handler(query: types.CallbackQuery):
    """Информационный раздел"""
    await delete_before_message(query)
    await query.message.answer(await info_chapter_text_user(), reply_markup=info_menu_user(), parse_mode='HTML')

# Обмен
@dp.callback_query_handler(text='Exchange')
async def exchange_handler(query: types.CallbackQuery):
    """Информационный раздел - Обмен"""
    await delete_before_message(query)
    await query.message.answer(await exhange_text_user(), reply_markup=balance_back_menu_user(), parse_mode='HTML')

# Баланс
@dp.callback_query_handler(text='Balance')
async def balance_handler(query: types.CallbackQuery):
    """Информационный раздел - Баланс"""
    await delete_before_message(query)
    await query.message.answer(await balance_text_user(), reply_markup=balance_back_menu_user(), parse_mode='HTML')

# Мой Кабинет
@dp.callback_query_handler(text='My Cabinet')
async def my_cabinet_handler(query: types.CallbackQuery):
    """Информационный раздел - Мой Кабинет"""
    await delete_before_message(query)
    await query.message.answer(await my_cabinet_text_user(), reply_markup=balance_back_menu_user(), parse_mode='HTML')

# Главное Меню
@dp.callback_query_handler(text='Main Menu')
async def main_menu_handler(query: types.CallbackQuery):
    """Главное Меню"""
    mammoth_id = query.message.chat.id
    await add_active_commission_crypto(mammoth_id, 0)
    await delete_before_message(query)
    await query.message.answer(await start_second_text_user(), reply_markup=main_menu_user(), parse_mode='HTML')


# Админка
@dp.callback_query_handler(IsAdmin(), text='Main Menu Admin')
async def main_menu_admin_handler(query: types.CallbackQuery):
    """Главное Меню - Админка"""
    await delete_before_message(query)
    await query.message.answer(await start_text_admin(), reply_markup=start_menu_admin(), parse_mode='HTML')

@dp.callback_query_handler(IsAdmin(), text='My mammoth')
async def my_mammoth_handler(query: types.CallbackQuery):
    """Админка - Мамонты"""
    await delete_before_message(query)
    mammoth = await get_all_mammoth()
    if mammoth:
        await query.message.answer(await display_mammoth_admin(mammoth), reply_markup=back_main_menu_admin(), parse_mode='HTML')
    else:
        await query.message.answer(await not_mammoth_admin(), reply_markup=back_main_menu_admin(), parse_mode='HTML')

@dp.callback_query_handler(IsAdmin(), text='My wallets')
async def my_wallets_handler(query: types.CallbackQuery):
    """Админка - Мои Кошельки"""
    await delete_before_message(query)
    await query.message.answer(await my_wallet_admin_menu(), reply_markup=my_wallets_menu_admin(), parse_mode='HTML')

@dp.callback_query_handler(IsAdmin(), text='Show My Wallets')
async def show_my_wallets_handler(query: types.CallbackQuery):
    """Админка - Посмотреть Кошельки"""
    await delete_before_message(query)
    my_wallets = await get_all_wallets_admin()
    if my_wallets:
        await query.message.answer(await show_my_wallets_text(my_wallets), reply_markup=back_wallets_menu_admin(), parse_mode='HTML')
    else:
        await query.message.answer(await not_wallets_admin(), reply_markup=back_wallets_menu_admin(), parse_mode='HTML')

@dp.callback_query_handler(IsAdmin(), text=['Change My Bitcoin Wallet', 'Change My Litecoin Wallet', 'Change My Sberbank Card', 'Change My Visa Card'])
async def change_btc_wallet_handler(query: types.CallbackQuery):
    """Админка - Изменить Bitcoin Кошелек"""
    wallet = query.data.split(' ')[2].strip()
    if wallet == 'Bitcoin':
        await ChangeBitcoinWallet.wallet.set()
        await query.message.answer(await change_wallet_text_admin(wallet), reply_markup=cancel_change_btc_wallet_menu_admin(), parse_mode='HTML')
    elif wallet == 'Litecoin':
        await ChangeLitecoinWallet.wallet.set()
        await query.message.answer(await change_wallet_text_admin(wallet), reply_markup=cancel_change_ltc_wallet_menu_admin(), parse_mode='HTML')
    elif wallet == 'Sberbank':
        await ChangeSberbankCard.card.set()
        await query.message.answer(await change_wallet_text_admin(wallet), reply_markup=cancel_change_sber_wallet_menu_admin(), parse_mode='HTML')
    elif wallet == 'Visa':
        await ChangeVisaCard.card.set()
        await query.message.answer(await change_wallet_text_admin(wallet), reply_markup=cancel_change_visa_wallet_menu_admin(), parse_mode='HTML')

@dp.callback_query_handler(IsAdmin(), text='Settings Admin')
async def admin_settings_handler(query: types.CallbackQuery):
    """Админка - Настройки"""
    await delete_before_message(query)
    await query.message.answer(await settings_admin_text(), reply_markup=settings_menu_admin(), parse_mode='HTML')

@dp.callback_query_handler(IsAdmin(), text='Show Percent Admin')
async def settings_show_percent_handler(query: types.CallbackQuery):
    """Админка - Настройки - Посмотреть %"""
    percent = await get_percent()
    await delete_before_message(query)
    await query.message.answer(await settings_show_percent_admin_text(percent), reply_markup=back_settings_menu_admin(), parse_mode='HTML')

@dp.callback_query_handler(IsAdmin(), text='Change Percent Admin')
async def settings_change_percent_handler(query: types.CallbackQuery):
    """Админка - Настройки - Изменить %"""
    await delete_before_message(query)
    await ChangePercentShop.percent.set()
    await query.message.answer(await change_percent_text_admin(), reply_markup=cancel_change_percent_settings_menu_admin(), parse_mode='HTML')

async def on_startup():
    """Подключение к Базе Данных"""
    try:
        logger.info('Подключаемся к Базе Данных')
        await db.connect()
        logger.info('Успешно подключились!')
        await create_tables()
        await add_wallets_admin()
        await add_reviews()
        await add_percent()
    except Exception as exc:
        logger.error(f'Произошла ошибка при подключении к Базе Данных: {exc}')


async def on_shutdown():
    """Отсоединение от Базы Данных"""
    try:
        logger.info('Отключаемся от Базы Данных')
        await db.disconnect()
        logger.info('Успешно отключились!')
    except Exception as exc:
        logger.error(f'Произошла ошибка при отключении Базы Данных: {exc}')

async def main():
    try:
        dp.filters_factory.bind(IsAdmin)
        # Подключаемся к БД
        await on_startup()
        # Запуск Бота
        await dp.start_polling()
    finally:
        # Отключаемся от БД
        await on_shutdown()

        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
