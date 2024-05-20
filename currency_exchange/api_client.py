import aiohttp
import asyncio
from datetime import datetime, timedelta

class PrivatBankAPIClient:
    BASE_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date="

    def __init__(self):
        pass

    async def fetch_exchange_rate(self, session, date):
        url = f"{self.BASE_URL}{date}"
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                return data
        except aiohttp.ClientError as e:
            print(f"HTTP error occurred: {e}")
            return None

    async def get_exchange_rates(self, days):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for day in range(days):
                date = (datetime.now() - timedelta(days=day)).strftime('%d.%m.%Y')
                tasks.append(self.fetch_exchange_rate(session, date))
            exchange_rates = await asyncio.gather(*tasks)
            return exchange_rates

