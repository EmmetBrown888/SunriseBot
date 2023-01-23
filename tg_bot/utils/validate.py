import re

from database.database import get_active_currency
from tg_bot.text.user import max_sum_btc, max_sum_ltc, min_sum_btc, min_sum_ltc
from tg_bot.keyboards.inline_user import cancel_enter_crypto_wallet_menu_user, sell_enter_card_menu_user
from tg_bot.keyboards.inline_admin import cancel_change_percent_settings_menu_admin


async def validate_form(form_field, message, currency=None):
    match form_field:
        case "bitcoin_wallet":
            pattern_btc = r'(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}'
            bitcoin = re.search(pattern_btc, message.text)
            if not bitcoin:
                await message.answer('Вы ввели некорректный Bitcoin-адрес!', reply_markup=cancel_enter_crypto_wallet_menu_user(), parse_mode='Markdown')
            else:
                return True
        case "litecoin_wallet":
            pattern_ltc = r'^ltc[a-km-zA-HJ-NP-Z1-9]{26,45}'
            litecoin = re.search(pattern_ltc, message.text)
            if not litecoin:
                await message.answer(f'Вы ввели некорректный Litecoin-адрес!', reply_markup=cancel_enter_crypto_wallet_menu_user(),  parse_mode='Markdown')
            else:
                return True
        case "ethereum_wallet":
            pattern_eth = r'0x[a-fA-F0-9]{40}'
            ethereum = re.search(pattern_eth, message.text)
            if not ethereum:
                await message.answer(f'Неправильный формат Ethereum кошелька!', parse_mode='Markdown')
            else:
                return True
        case "tether_wallet":
            pattern_usdt_trc20 = r'T[A-Za-z1-9]{33}'
            tether_trc20 = re.search(pattern_usdt_trc20, message.text)
            if not tether_trc20:
                await message.answer(f'Неправильный формат USDT TRC20 кошелька!', parse_mode='Markdown')
            else:
                return True
        case "card_number":
            if not message.text.isdigit():
                await message.answer(f'Вы ввели некорректные свои банковские реквизиты!', reply_markup=sell_enter_card_menu_user(), parse_mode='Markdown')
            elif not len(message.text) == 16:
                await message.answer(f'Вы ввели некорректные свои банковские реквизиты!', reply_markup=sell_enter_card_menu_user(), parse_mode='Markdown')
            else:
                return True
        case "amount_crypto":
            if currency == 'Bitcoin':
                symbol = 'BTC'
                print('1')
                print('type(message.text): ', type(message.text))
                try:
                    if float(message.text):
                        print('2')
                        if float(min_sum_btc) <= float(message.text) and float(message.text) <= float(max_sum_btc):
                            print('3')
                            return True
                        else:
                            print('4')
                            await message.answer(f"👛 На какую сумму Вы хотите купить {currency}?\n\n(Напишите сумму: от {min_sum_btc} до {max_sum_btc} {symbol})")
                except ValueError:
                    await message.answer(f"👛 На какую сумму Вы хотите купить {currency}?\n\n(Напишите сумму: от {min_sum_btc} до {max_sum_btc} {symbol})")
            elif currency == 'Litecoin':
                symbol = 'LTC'
                try:
                    if float(message.text):
                        if float(min_sum_ltc) <= float(message.text) and float(message.text) <= float(max_sum_ltc):
                            return True
                        else:
                            await message.answer(f"👛 На какую сумму Вы хотите купить {currency}?\n\n(Напишите сумму: от {min_sum_ltc} до {max_sum_ltc} {symbol})")
                except ValueError:
                    await message.answer(f"👛 На какую сумму Вы хотите купить {currency}?\n\n(Напишите сумму: от {min_sum_ltc} до {max_sum_ltc} {symbol})")
        case "sell_amount_crypto":
            if currency == 'Bitcoin':
                symbol = 'BTC'
                print('1')
                print('type(message.text): ', type(message.text))
                try:
                    if float(message.text):
                        print('2')
                        if float(min_sum_btc) <= float(message.text) and float(message.text) <= float(max_sum_btc):
                            print('3')
                            return True
                        else:
                            print('4')
                            await message.answer(f"👛 На какую сумму Вы хотите продать {currency}?\n\n(Напишите сумму: от {min_sum_btc} до {max_sum_btc} {symbol})")
                except ValueError:
                    await message.answer(f"👛 На какую сумму Вы хотите продать {currency}?\n\n(Напишите сумму: от {min_sum_btc} до {max_sum_btc} {symbol})")
            elif currency == 'Litecoin':
                symbol = 'LTC'
                try:
                    if float(message.text):
                        if float(min_sum_ltc) <= float(message.text) and float(message.text) <= float(max_sum_ltc):
                            return True
                        else:
                            await message.answer(f"👛 На какую сумму Вы хотите продать {currency}?\n\n(Напишите сумму: от {min_sum_ltc} до {max_sum_ltc} {symbol})")
                except ValueError:
                    await message.answer(f"👛 На какую сумму Вы хотите продать {currency}?\n\n(Напишите сумму: от {min_sum_ltc} до {max_sum_ltc} {symbol})")
        case "percent":
            try:
                if int(message.text):
                    return True
                else:
                    await message.answer(f'Вы ввели некорректный Процент!', reply_markup=cancel_change_percent_settings_menu_admin(), parse_mode='Markdown')
            except ValueError:
                await message.answer(f'Вы ввели некорректный Процент!', reply_markup=cancel_change_percent_settings_menu_admin(), parse_mode='Markdown')
        case _:
            pass
