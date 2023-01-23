from databases import Database

from tg_bot.settings import logger

db = Database('sqlite+aiosqlite:///mydatabase.db')


async def create_tables():
    """Создания Таблиц"""
    try:
        # Создаем Таблицу Мамонты
        await db.execute("""CREATE TABLE IF NOT EXISTS mammoth
                            (
                                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                mammoth_id BIGINT NOT NULL,
                                choose_currency VARCHAR(15) DEFAULT NULL,
                                choose_amount_crypto NUMERIC(100,8) DEFAULT NULL,
                                choose_amount_ruble FLOAT DEFAULT NULL,
                                choose_type_card VARCHAR(10) DEFAULT NULL,
                                code_word VARCHAR(100) DEFAULT NULL,
                                help_text VARCHAR(1000) DEFAULT NULL,
                                wallet_crypto VARCHAR(100) DEFAULT NULL,
                                amount_commission INTEGER DEFAULT 0,
                                card_number VARCHAR(16) DEFAULT NULL,
                                mammoth_username VARCHAR(255) NOT NULL
                        )
        """)

        # Создаем Таблицу Баланс Мамонта
        await db.execute("""CREATE TABLE IF NOT EXISTS balance
                            (
                                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                mammoth_id BIGINT NOT NULL,
                                ruble NUMERIC(7,0) DEFAULT 0,
                                bitcoin NUMERIC(100,8) DEFAULT 0.00000000,
                                litecoin NUMERIC(100,8) DEFAULT 0.00000000
                        )
        """)
        # Создаем Таблицу Курса Валют
        await db.execute("""CREATE TABLE IF NOT EXISTS rate_currencies
                            (
                                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                symbol VARCHAR(10) NOT NULL,
                                amount FLOAT NOT NULL
                        )
        """)
        # Создаем Таблицу Кошельки Админа
        await db.execute("""CREATE TABLE IF NOT EXISTS wallets_admin
                            (
                                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                name VARCHAR(15) NOT NULL,
                                value VARCHAR(255) NOT NULL
                        )
        """)
        # Создаем Таблицу Отзывы
        await db.execute("""CREATE TABLE IF NOT EXISTS reviews
                            (
                                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                author VARCHAR(50) NOT NULL,
                                text TEXT NOT NULL
                        )
        """)
        # Создаем Таблицу Процент Магазина
        await db.execute("""CREATE TABLE IF NOT EXISTS percent
                            (
                                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                value INTEGER DEFAULT 10
                        )
        """)
    except Exception as exc:
        logger.error(f"Exception create_tables:  {exc}")


async def add_mammoth(mammoth_id, username):
    """Добавление Мамонта"""
    try:
        mammoth = await db.fetch_one(
            query=f'SELECT * FROM mammoth WHERE mammoth_id=:mammoth_id;',
            values={
                'mammoth_id': mammoth_id
            }
        )

        if not mammoth:
            await db.execute(
                query="INSERT INTO mammoth(mammoth_id, mammoth_username) VALUES(:mammoth_id, :mammoth_username);",
                values={
                    'mammoth_id': mammoth_id,
                    'mammoth_username': username
                }
            )
            await db.execute(
                query="INSERT INTO balance(mammoth_id) VALUES(:mammoth_id);",
                values={
                    'mammoth_id': mammoth_id
                }
            )
    except Exception as exc:
        logger.error(f"Exception add_mammoth: {exc}")


async def get_all_mammoth():
    """Получение всех мамонтов"""
    try:
        mammoth = await db.fetch_all(query=f'SELECT * FROM mammoth;')
        if mammoth:
            return mammoth
    except Exception as exc:
        logger.error(f"Exception get_all_mammoth: {exc}") 


async def get_id_mammoth(mammoth_id):
    """Получение ID мамонта"""
    try:
        mammoth = await db.fetch_one(
            query=f'SELECT * FROM mammoth WHERE mammoth_id=:mammoth_id;',
            values={
                'mammoth_id': mammoth_id
            }
        )

        if mammoth:
            return mammoth[0]
    except Exception as exc:
        logger.error(f"Exception get_id_mammoth: {exc}")


async def add_active_currency(mammoth_id, choose_currency):
    """Добавление Активной Валюты"""
    try:
        mammoth = await db.fetch_one(
            query=f'SELECT * FROM mammoth WHERE mammoth_id=:mammoth_id;',
            values={
                'mammoth_id': mammoth_id
            }
        )

        if mammoth:
            await db.execute(
                query=f"UPDATE mammoth SET choose_currency=:choose_currency WHERE mammoth_id=:mammoth_id;",
                values={
                    'mammoth_id': mammoth_id,
                    'choose_currency': str(choose_currency)
                }
            )
    except Exception as exc:
        logger.error(f"Exception add_active_currency:  {exc}")


async def add_code_word(mammoth_id, code_word):
    """Добавление Кодового Слова"""
    try:
        mammoth = await db.fetch_one(
            query=f'SELECT * FROM mammoth WHERE mammoth_id=:mammoth_id;',
            values={
                'mammoth_id': mammoth_id
            }
        )

        if mammoth:
            await db.execute(
                query=f"UPDATE mammoth SET code_word=:code_word WHERE mammoth_id=:mammoth_id;",
                values={
                    'mammoth_id': mammoth_id,
                    'code_word': code_word
                }
            )
    except Exception as exc:
        logger.error(f"Exception add_code_word:  {exc}")


async def add_help_text_word(mammoth_id, help_text):
    """Добавление Подсказки к коду"""
    try:
        mammoth = await db.fetch_one(
            query=f'SELECT * FROM mammoth WHERE mammoth_id=:mammoth_id;',
            values={
                'mammoth_id': mammoth_id
            }
        )

        if mammoth:
            await db.execute(
                query=f"UPDATE mammoth SET help_text=:help_text WHERE mammoth_id=:mammoth_id;",
                values={
                    'mammoth_id': mammoth_id,
                    'help_text': help_text
                }
            )
    except Exception as exc:
        logger.error(f"Exception add_help_text_word:  {exc}")


async def get_help_text(mammoth_id):
    """Получения Слова подсказка"""
    try:
        mammoth = await db.fetch_one(
            query=f'SELECT * FROM mammoth WHERE mammoth_id=:mammoth_id;',
            values={
                'mammoth_id': mammoth_id
            }
        )

        if mammoth:
            return mammoth[7]
    except Exception as exc:
        logger.error(f"Exception get_help_text:  {exc}")


async def delete_help_text(mammoth_id):
    """Удаление Слова Подсказка"""
    try:
        mammoth = await db.fetch_one(
            query=f'SELECT * FROM mammoth WHERE mammoth_id=:mammoth_id;',
            values={
                'mammoth_id': mammoth_id
            }
        )

        if mammoth:
            await db.execute(
                query=f"UPDATE mammoth SET help_text=:help_text WHERE mammoth_id=:mammoth_id;",
                values={
                    'mammoth_id': mammoth_id,
                    'help_text': None
                }
            )
    except Exception as exc:
        logger.error(f"Exception delete_help_text:  {exc}")


async def get_code_word(mammoth_id):
    """Получения Кодового Слова"""
    try:
        mammoth = await db.fetch_one(
            query=f'SELECT * FROM mammoth WHERE mammoth_id=:mammoth_id;',
            values={
                'mammoth_id': mammoth_id
            }
        )

        if mammoth:
            return mammoth[6]
    except Exception as exc:
        logger.error(f"Exception get_code_word:  {exc}")


async def check_exist_code_word(mammoth_id, code_word):
    """Проверка Кодового Слова"""
    try:
        mammoth = await db.fetch_one(
            query=f'SELECT * FROM mammoth WHERE mammoth_id=:mammoth_id and code_word=:code_word;',
            values={
                'mammoth_id': mammoth_id,
                'code_word': code_word
            }
        )

        if mammoth:
            return True
        else:
            return False
    except Exception as exc:
        logger.error(f"Exception check_exist_code_word:  {exc}")


async def delete_code_word(mammoth_id):
    """Удаление Кодового Слова"""
    try:
        mammoth = await db.fetch_one(
            query=f'SELECT * FROM mammoth WHERE mammoth_id=:mammoth_id;',
            values={
                'mammoth_id': mammoth_id
            }
        )

        if mammoth:
            await db.execute(
                query=f"UPDATE mammoth SET code_word=:code_word WHERE mammoth_id=:mammoth_id;",
                values={
                    'mammoth_id': mammoth_id,
                    'code_word': None
                }
            )
    except Exception as exc:
        logger.error(f"Exception delete_code_word:  {exc}")


async def add_active_type_card(mammoth_id, choose_type_card):
    """Добавление Выбранной Типа Карты"""
    try:
        mammoth = await db.fetch_one(
            query=f'SELECT * FROM mammoth WHERE mammoth_id=:mammoth_id;',
            values={
                'mammoth_id': mammoth_id
            }
        )

        if mammoth:
            await db.execute(
                query=f"UPDATE mammoth SET choose_type_card=:choose_type_card WHERE mammoth_id=:mammoth_id;",
                values={
                    'mammoth_id': mammoth_id,
                    'choose_type_card': choose_type_card
                }
            )
    except Exception as exc:
        logger.error(f"Exception add_active_type_card:  {exc}")


async def get_active_type_card(mammoth_id):
    """Получение Выбранной Типа Карты"""
    try:
        mammoth = await db.fetch_one(
            query=f'SELECT * FROM mammoth WHERE mammoth_id=:mammoth_id;',
            values={
                'mammoth_id': mammoth_id
            }
        )

        if mammoth:
            return mammoth[5]
    except Exception as exc:
        logger.error(f"Exception get_active_type_card:  {exc}")


async def get_balance(mammoth_id):
    """Получение Баланса"""
    try:
        mammoth = await db.fetch_one(
            query=f'SELECT * FROM balance WHERE mammoth_id=:mammoth_id;',
            values={
                'mammoth_id': mammoth_id
            }
        )

        if mammoth:
            return mammoth
    except Exception as exc:
        logger.error(f"Exception get_balance:  {exc}") 


async def get_active_currency(mammoth_id):
    """Получение Активной Валюты"""
    try:
        active_currency = await db.fetch_one(
            query=f'SELECT * FROM mammoth WHERE mammoth_id=:mammoth_id;',
            values={
                'mammoth_id': mammoth_id
            }
        )

        if active_currency:
            return active_currency[2]
    except Exception as exc:
        logger.error(f"Exception get_balance:  {exc}")


async def add_active_crypto_amount(mammoth_id, amount):
    """Добавление Активной цены Crypto"""
    try:
        mammoth = await db.fetch_one(
            query=f'SELECT * FROM mammoth WHERE mammoth_id=:mammoth_id;',
            values={
                'mammoth_id': mammoth_id
            }
        )

        if mammoth:
            await db.execute(
                query=f"UPDATE mammoth SET choose_amount_crypto=:choose_amount_crypto WHERE mammoth_id=:mammoth_id;",
                values={
                    'mammoth_id': mammoth_id,
                    'choose_amount_crypto': amount
                }
            )
    except Exception as exc:
        logger.error(f"Exception add_active_crypto_amount:  {exc}")

async def get_active_crypto_amount(mammoth_id):
    """Получение Активной цены Crypto"""
    try:
        mammoth = await db.fetch_one(
            query=f'SELECT * FROM mammoth WHERE mammoth_id=:mammoth_id;',
            values={
                'mammoth_id': mammoth_id
            }
        )

        if mammoth:
            return mammoth[3]
    except Exception as exc:
        logger.error(f"Exception add_active_crypto_amount:  {exc}")


async def add_active_ruble_amount(mammoth_id, amount):
    """Добавление Активной цены Ruble"""
    try:
        mammoth = await db.fetch_one(
            query=f'SELECT * FROM mammoth WHERE mammoth_id=:mammoth_id;',
            values={
                'mammoth_id': mammoth_id
            }
        )

        if mammoth:
            await db.execute(
                query=f"UPDATE mammoth SET choose_amount_ruble=:choose_amount_ruble WHERE mammoth_id=:mammoth_id;",
                values={
                    'mammoth_id': mammoth_id,
                    'choose_amount_ruble': amount
                }
            )
    except Exception as exc:
        logger.error(f"Exception add_active_ruble_amount:  {exc}")


async def get_active_ruble_amount(mammoth_id):
    """Получение Активной цены Рубль"""
    try:
        mammoth = await db.fetch_one(
            query=f'SELECT * FROM mammoth WHERE mammoth_id=:mammoth_id;',
            values={
                'mammoth_id': mammoth_id
            }
        )

        if mammoth:
            return mammoth[4]
    except Exception as exc:
        logger.error(f"Exception get_active_rubble_amount:  {exc}")

# Курсы Валют
async def get_rate_crypto(symbol):
    """Получение Курсы Валют"""
    try:
        rate = await db.fetch_one(
            query=f'SELECT * FROM rate_currencies WHERE symbol=:symbol;',
            values={
                'symbol': f'{symbol}RUB'
            }
        )
        if rate:
            return rate
    except Exception as exc:
        logger.error(f"Exception rate:  {exc}")


# Кошельки Админа
async def add_wallets_admin():
    """Добавление кошельков заглушек Админа"""
    try:
        wallets = await db.fetch_one(query='SELECT * from wallets_admin WHERE EXISTS (SELECT * from wallets_admin);')
        if not wallets:
            await db.execute(
                query="INSERT INTO wallets_admin(name, value) VALUES(:name, :value);",
                values={
                    'name': 'bitcoin',
                    'value': '1111111111111111'
                }
            )
            await db.execute(
                query="INSERT INTO wallets_admin(name, value) VALUES(:name, :value);",
                values={
                    'name': 'litecoin',
                    'value': '2222222222222222'
                }
            )
            await db.execute(
                query="INSERT INTO wallets_admin(name, value) VALUES(:name, :value);",
                values={
                    'name': 'sberbank',
                    'value': '3333333333333333'
                }
            )
            await db.execute(
                query="INSERT INTO wallets_admin(name, value) VALUES(:name, :value);",
                values={
                    'name': 'visa',
                    'value': '4444444444444444'
                }
            )
    except Exception as exc:
        logger.error(f'Exception add_wallets_admin: {exc}')


async def get_wallets_admin(currency):
    """Получение Кошелька Админа"""
    try:
        wallet = await db.fetch_one(
            query='SELECT * from wallets_admin WHERE name=:name;',
            values={
                'name': currency.lower()
            }
        )
        print('wallet: ', wallet)
        if wallet:
            return wallet
    except Exception as exc:
        logger.error(f'Exception get_wallets_admin: {exc}')


async def get_all_wallets_admin():
    """Получение Кошельков Админа"""
    try:
        wallets = await db.fetch_all(query='SELECT * from wallets_admin;')
        if wallets:
            return wallets
    except Exception as exc:
        logger.error(f'Exception get_all_wallets_admin: {exc}')


async def change_wallet_admin(name, value):
    """Изменение Кошелька Админа"""
    try:
        wallet = await db.fetch_one(
            query=f'SELECT * FROM wallets_admin WHERE name=:name;',
            values={
                'name': name
            }
        )
        if wallet:
            await db.execute(
                query=f"UPDATE wallets_admin SET value=:value WHERE name=:name;",
                values={
                    'name': name,
                    'value': value
                }
            )
    except Exception as exc:
        logger.error(f'Exception change_wallet_admin: {exc}')

# Reviews
async def add_reviews():
    """Добавление Отзывов"""
    try:
        wallets = await db.fetch_one(query='SELECT * from reviews WHERE EXISTS (SELECT * from reviews);')
        if not wallets:
            await db.execute(
                query="INSERT INTO reviews(author, text) VALUES(:author, :text);",
                values={
                    'author': 'Дмитрий',
                    'text': 'пользуюсь данным обменником и радуюсь вы молодцы успехов вам😉👍👍👍'
                }
            )
            await db.execute(
                query="INSERT INTO reviews(author, text) VALUES(:author, :text);",
                values={
                    'author': 'Ебальники',
                    'text': 'Good'
                }
            )
            await db.execute(
                query="INSERT INTO reviews(author, text) VALUES(:author, :text);",
                values={
                    'author': 'Матвей',
                    'text': 'Как обычно - всë отлично! Всем советую! 🤙🏻'
                }
            )
            await db.execute(
                query="INSERT INTO reviews(author, text) VALUES(:author, :text);",
                values={
                    'author': 'левый',
                    'text': 'чудесно'
                }
            )
            await db.execute(
                query="INSERT INTO reviews(author, text) VALUES(:author, :text);",
                values={
                    'author': 'Rtyyyu',
                    'text': 'Чётко'
                }
            )
            await db.execute(
                query="INSERT INTO reviews(author, text) VALUES(:author, :text);",
                values={
                    'author': 'Семен',
                    'text': 'Я бешено сквиртую от этого возбуждающегообменника!!!'
                }
            )
            await db.execute(
                query="INSERT INTO reviews(author, text) VALUES(:author, :text);",
                values={
                    'author': 'Igor',
                    'text': ' Обмен прошёл очень быстро! Спасибо большое 👍'
                }
            )
            await db.execute(
                query="INSERT INTO reviews(author, text) VALUES(:author, :text);",
                values={
                    'author': 'Лапочка',
                    'text': 'Всё отлично'
                }
            )
            await db.execute(
                query="INSERT INTO reviews(author, text) VALUES(:author, :text);",
                values={
                    'author': 'Милана',
                    'text': 'Все круто'
                }
            )
            await db.execute(
                query="INSERT INTO reviews(author, text) VALUES(:author, :text);",
                values={
                    'author': 'iKirsh',
                    'text': '0.0555 обменял за секунды. Надёжный обменник. Советую'
                }
            )
    except Exception as exc:
        logger.error(f'Exception add_wallets_admin: {exc}')


async def get_reviews():
    """Получение отзывов"""
    try:
        reviews = await db.fetch_all(query='SELECT * from reviews LIMIT 10;')
        if reviews:
            return reviews
    except Exception as exc:
        logger.error(f'Exception get_reviews: {exc}')


async def get_review(id_review):
    """Получить отзыв"""
    try:
        review = await db.fetch_one(query='SELECT * from reviews WHERE id=:id;', values={'id': int(id_review)})
        if review:
            return review
    except Exception as exc:
        logger.error(f'Exception get_review: {exc}')

# Активный кошелек
async def add_wallet_crypto(mammoth_id, wallet_crypto):
    """Добавление Активного Крипто Кошелько"""
    try:
        mammoth = await db.fetch_one(
            query=f'SELECT * FROM mammoth WHERE mammoth_id=:mammoth_id;',
            values={
                'mammoth_id': mammoth_id
            }
        )
        if mammoth:
            await db.execute(
                query=f"UPDATE mammoth SET wallet_crypto=:wallet_crypto WHERE mammoth_id=:mammoth_id;",
                values={
                    'mammoth_id': mammoth_id,
                    'wallet_crypto': wallet_crypto
                }
            )
    except Exception as exc:
        logger.error(f'Exception add_wallet_crypto: {exc}')


async def get_active_wallet_crypto(mammoth_id):
    """Получение Активного Крипто Кошелька"""
    try:
        mammoth = await db.fetch_one(
            query=f'SELECT * FROM mammoth WHERE mammoth_id=:mammoth_id;',
            values={
                'mammoth_id': mammoth_id
            }
        )

        if mammoth:
            return mammoth[8]
    except Exception as exc:
        logger.error(f"Exception get_active_wallet_crypto:  {exc}")

# Коммиссия
async def add_active_commission_crypto(mammoth_id, amount_commission):
    """Добавление Активной Коммиссии"""
    try:
        mammoth = await db.fetch_one(
            query=f'SELECT * FROM mammoth WHERE mammoth_id=:mammoth_id;',
            values={
                'mammoth_id': mammoth_id
            }
        )
        if mammoth:
            await db.execute(
                query=f"UPDATE mammoth SET amount_commission=:amount_commission WHERE mammoth_id=:mammoth_id;",
                values={
                    'mammoth_id': mammoth_id,
                    'amount_commission': amount_commission
                }
            )
    except Exception as exc:
        logger.error(f'Exception add_active_commission_crypto: {exc}')


async def get_active_commission_crypto(mammoth_id):
    """Получение Активной Коммиссии"""
    try:
        mammoth = await db.fetch_one(
            query=f'SELECT * FROM mammoth WHERE mammoth_id=:mammoth_id;',
            values={
                'mammoth_id': mammoth_id
            }
        )

        if mammoth:
            return mammoth[9]
    except Exception as exc:
        logger.error(f"Exception get_active_commission_crypto:  {exc}")

# Реквизиты Карты
async def add_active_card_number(mammoth_id, card_number):
    """Добавление Активной Карты"""
    try:
        mammoth = await db.fetch_one(
            query=f'SELECT * FROM mammoth WHERE mammoth_id=:mammoth_id;',
            values={
                'mammoth_id': mammoth_id
            }
        )
        if mammoth:
            await db.execute(
                query=f"UPDATE mammoth SET card_number=:card_number WHERE mammoth_id=:mammoth_id;",
                values={
                    'mammoth_id': mammoth_id,
                    'card_number': str(card_number)
                }
            )
    except Exception as exc:
        logger.error(f'Exception add_active_card_number: {exc}')


async def get_active_card_number(mammoth_id):
    """Получение Активной Коммиссии"""
    try:
        mammoth = await db.fetch_one(
            query=f'SELECT * FROM mammoth WHERE mammoth_id=:mammoth_id;',
            values={
                'mammoth_id': mammoth_id
            }
        )

        if mammoth:
            return mammoth[10]
    except Exception as exc:
        logger.error(f"Exception get_active_card_number:  {exc}")

# Процент
async def add_percent():
    """Добавление Процента"""
    try:
        percent = await db.fetch_one(
            query=f'SELECT * FROM percent WHERE id=:id;',
            values={
                'id': 1
            }
        )

        if not percent:
            await db.execute(
                query=f"INSERT INTO percent(value) VALUES(:value);",
                values={
                    'value': 10
                }
            )
    except Exception as exc:
        logger.error(f"Exception add_percent:  {exc}")



async def get_percent():
    """Получение Процента"""
    try:
        percent = await db.fetch_one(
            query=f'SELECT * FROM percent WHERE id=:id;',
            values={
                'id': 1
            }
        )

        if percent:
            return percent[1]
    except Exception as exc:
        logger.error(f"Exception get_percent:  {exc}")


async def change_percent(percent_num):
    """Изменение Процента"""
    try:
        
        percent = await db.fetch_one(
            query=f'SELECT * FROM percent WHERE id=:id;',
            values={
                'id': 1
            }
        )
        if percent:
            await db.execute(
                query=f"UPDATE percent SET value=:value WHERE id=:id;",
                values={
                    'id': 1,
                    'value': int(percent_num)
                }
            )
    except Exception as exc:
        logger.error(f'Exception change_percent: {exc}')