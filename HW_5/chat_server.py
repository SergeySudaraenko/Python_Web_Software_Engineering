import sys
import asyncio
import websockets
import json
import os
from datetime import datetime

# Отримуємо шлях до поточного каталогу
current_dir = os.path.dirname(os.path.abspath(__file__))

# Додаємо каталог currency_exchange до шляху пошуку Python
currency_exchange_dir = os.path.join(current_dir, 'currency_exchange')
sys.path.append(currency_exchange_dir)

# Імпортуємо клас з модуля api_client
from currency_exchange.api_client import PrivatBankAPIClient
from currency_exchange.utils import extract_currency_data
from currency_exchange.main import main

connected_clients = set()

async def log_to_file(message):
    async with AIOFile("exchange_log.txt", 'a') as afp:
        writer = Writer(afp)
        await writer(f"{datetime.now()}: {message}\n")

async def handle_client(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            if message.startswith("exchange"):
                parts = message.split()
                days = int(parts[1]) if len(parts) > 1 else 1
                currencies = parts[2:] if len(parts) > 2 else ["USD", "EUR"]

                if days > 10:
                    response = "Ви можете запитати курс валют не більше, ніж за останні 10 днів."
                else:
                    client = PrivatBankAPIClient()
                    data = await client.get_exchange_rates(days)
                    rates = extract_currency_data(data, currencies)
                    response = json.dumps(rates, ensure_ascii=False, indent=2)

                await websocket.send(response)
                await log_to_file(f"Command: {message} - Response: {response}")
            else:
                await websocket.send("Unknown command")
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handle_client, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())






