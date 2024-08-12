import asyncio
import os
import sys
import httpx
import random
import time
import uuid
from loguru import logger

httpx_log = logger.bind(name="httpx").level("WARNING")
logger.remove()
logger.add(sink=sys.stdout, format="<white>{time:YYYY-MM-DD HH:mm:ss}</white>"
                   " | <level>{level: <8}</level>"
                   " | <cyan><b>{line}</b></cyan>"
                   " - <white><b>{message}</b></white>")
logger = logger.opt(colors=True)

games = {
    1: {
        'name': 'Riding Extreme 3D',
        'appToken': 'd28721be-fd2d-4b45-869e-9f253b554e50', 
        'promoId': '43e35910-c168-4634-ad4f-52fd764a843f',
    },
    2: {
        'name': 'Chain Cube 2048',
        'appToken': 'd1690a07-3780-4068-810f-9b5bbf2931b2', 
        'promoId': 'b4170868-cef0-424f-8eb9-be0622e8e8e3',
    },
    3: {
        'name': 'My Clone Army',
        'appToken': '74ee0b5b-775e-4bee-974f-63e7f4d5bacb', 
        'promoId': 'fe693b26-b342-4159-8808-15e3ff7f8767',
    },
    4: {
        'name': 'Train Miner',
        'appToken': '82647f43-3f87-402d-88dd-09a90025313f', 
        'promoId': 'c4480ac7-e178-4973-8061-9ed5b2e17954',
    }
}

EVENTS_DELAY = 20000 / 1000

async def load_proxies(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                proxies = [line.strip() for line in file if line.strip()]
                random.shuffle(proxies)
                return proxies
        else:
            logger.info(f"Proxy file {file_path} not found. No proxies will be used.")
            return []
    except Exception as e:
        logger.error(f"Error reading proxy file {file_path}: {e}")
        return []

async def generate_client_id():
    timestamp = int(time.time() * 1000)
    random_numbers = ''.join(str(random.randint(0, 30)) for _ in range(30))
    return f"{timestamp}-{random_numbers}"

async def login(client_id, app_token, proxies, retries=5):
    for attempt in range(retries):
        proxy = random.choice(proxies) if proxies else None
        async with httpx.AsyncClient(proxies=proxy) as client:
            try:
                logger.info(f"Attempting to log in with client ID: {client_id} (Attempt {attempt + 1}/{retries})")
                response = await client.post(
                    'https://api.gamepromo.io/promo/login-client',
                    json={'appToken': app_token, 'clientId': client_id, 'clientOrigin': 'deviceid'}
                )
                response.raise_for_status()
                data = response.json()
                logger.info(f"Login successful for client ID: {client_id}")
                return data['clientToken']
            except httpx.HTTPStatusError as e:
                logger.error(f"Failed to login (attempt {attempt + 1}/{retries}): {e.response.json()}")
            except Exception as e:
                logger.error(f"Unexpected error during login (attempt {attempt + 1}/{retries}): {e}")
        await asyncio.sleep(2)
    logger.error("Maximum login attempts reached. Returning None.")
    return None

async def emulate_progress(client_token, promo_id, proxies):
    proxy = random.choice(proxies) if proxies else None
    logger.info(f"Emulating progress for promo ID: {promo_id}")
    async with httpx.AsyncClient(proxies=proxy) as client:
        response = await client.post(
            'https://api.gamepromo.io/promo/register-event',
            headers={'Authorization': f'Bearer {client_token}'},
            json={'promoId': promo_id, 'eventId': str(uuid.uuid4()), 'eventOrigin': 'undefined'}
        )
        response.raise_for_status()
        data = response.json()
        return data['hasCode']

async def generate_key(client_token, promo_id, proxies):
    # Placeholder - you'll need to implement the key generation logic
    print(f"Generating key for promo ID: {promo_id}") 

async def main():
    proxies = await load_proxies("proxies.txt") # Replace 'proxies.txt' if needed

    for game_id, game_data in games.items():
        logger.info(f"Processing game: {game_data['name']}")
        client_id = await generate_client_id()
        client_token = await login(client_id, game_data['appToken'], proxies)

        if client_token:
            has_code = await emulate_progress(client_token, game_data['promoId'], proxies)
            if has_code:
                await generate_key(client_token, game_data['promoId'], proxies) 

if __name__ == '__main__':
    asyncio.run(main())
