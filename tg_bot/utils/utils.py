async def send_message(bot, chat_id, message):
    """Отправка сообщения"""

    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except Exception as exc:
        print('Exception send_message: ', exc)
