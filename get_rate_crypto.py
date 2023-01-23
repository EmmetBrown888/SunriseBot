import asyncio
import requests

from databases import Database

async def add_rate_crypto(symbol, amount):
    try:
        db = Database('sqlite+aiosqlite:///mydatabase.db')
        
        rate = await db.fetch_one(
            query=f'SELECT * FROM rate_currencies WHERE symbol=:symbol;',
            values={
                'symbol': symbol
            }
        )
        if rate:
            await db.execute(
                query=f"UPDATE rate_currencies SET amount=:amount WHERE symbol=:symbol;",
                values={'amount': amount, 'symbol': symbol}
            )
        else:            
            await db.execute(
                query="INSERT INTO rate_currencies(symbol, amount) VALUES(:symbol, :amount);",
                values={'symbol': symbol, 'amount': amount}
            )
        
    except Exception as exc:
        print('Exception: add_rate_crypto: ', exc)
  
# defining key/request 
# print(f"{data['symbol']} price is {data['price']}")

async def run():
    try:
        url = 'https://api.binance.com/api/v1/ticker/24hr?symbols=[%22BTCRUB%22,%22LTCRUB%22]'  
        res = requests.get(url)  
        if res.status_code == 200:
            for symbol in res.json():
                # print(f"{symbol['symbol']}: ", symbol['lastPrice'])
                await add_rate_crypto(symbol['symbol'], symbol['lastPrice'])
        else:
            print('Ошибка при обращении к API Binance!')
    except Exception as exc:
        print('Exception run: ', exc)

if __name__ == '__main__':
    asyncio.run(run())
