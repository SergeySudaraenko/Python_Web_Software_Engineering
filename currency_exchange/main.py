import sys
import asyncio
from datetime import datetime, timedelta
import json
import os

# Додаємо підкаталог HW_5 в sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'HW_5'))

from api_client import PrivatBankAPIClient
from utils import extract_currency_data

async def main(days, currencies):
    client = PrivatBankAPIClient()
    data = await client.get_exchange_rates(days)
    rates = extract_currency_data(data, currencies)
    print(json.dumps(rates, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <days> [<currency1> <currency2> ...]")
        sys.exit(1)

    days = int(sys.argv[1])
    currencies = sys.argv[2:] if len(sys.argv) > 2 else ["USD", "EUR"]

    if days > 10:
        print("Ви можете запитати курс валют не більше, ніж за останні 10 днів.")
        sys.exit(1)

    asyncio.run(main(days, currencies))

