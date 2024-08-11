```
import asyncio
import os
import sys
import httpx
import random
import time
import uuid
import json
from loguru import logger

# Disable logging for httpx
httpx_log = logger.bind(name="httpx").level("WARNING")
logger.remove()
logger.add(sink=sys.stdout, format="<white>{time:YYYY-MM-DD HH:mm:ss}</white>" 
                                  " | <level>{level: <8}</level>" 
                                  " | <cyan><b>{line}</b></cyan>" 
                                  " - <white><b>{message}</b></white>")
logger = logger.opt(colors=True)

# Game configuration
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

# Constants
EVENTS_DELAY = 20000 / 1000  # converting milliseconds to seconds
MAX_LOGIN_ATTEMPTS = 5
PROXY_FILE = 'proxy.txt'

# Load proxies from file
async def load_proxies(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                proxies = [line.strip() for line in file if line.strip()]
                random.shuffle(proxies)  # Shuffle proxies to ensure randomness
                return proxies
        else:
            logger.info(f"Proxy file {file_path} not found. No proxies will be used.")
            return []
    except Exception as e:
        logger.error(f"Error reading proxy file {file_path}: {e}")
        return []

# Generate client ID
async def generate_client_id():
    timestamp = int(time.time() * 1000)
    random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(19))
    return f"{timestamp}-{random_numbers}"

# Login to game
async def login(client_id, app_token, proxies):
    for attempt in range(MAX_LOGIN_ATTEMPTS):
        proxy = random.choice(proxies) if proxies else None
        async with httpx.AsyncClient(proxies=proxy, timeout=30.0) as client:
            try:
                logger.info(f"Attempting to log in with client ID: {client_id} (Attempt {attempt + 1}/{MAX_LOGIN_ATTEMPTS})")
                response = await client.post(
                    'https://api.gamepromo.io/promo/login-client',
                    json={'appToken': app_token, 'clientId': client_id, 'clientOrigin': 'deviceid'}
                )
                response.raise_for_status()
                try:
                    data = response.json()
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error: {e}")
                    continue
                logger.info(f"Login successful for client ID: {client_id}")
                return data['clientToken']
            except httpx.HTTPStatusError as e:
                logger.error(f"Failed to login (attempt {attempt + 1}/{MAX_LOGIN_ATTEMPTS}): {e.response.json()}")
            except Exception as e:
                logger.error(f"Unexpected error during login (attempt {attempt + 1}/{MAX_LOGIN_ATTEMPTS}): {e}")
            await asyncio.sleep(2)  #
```There was a problem generating a response. Please try again later.
