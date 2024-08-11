import asyncio
import uuid

async def generate_keys(games):
    for game_id, game_data in games.items():
        app_token = game_data['appToken']
        promo_id = game_data['promoId']
        game_name = game_data['name']

        # Generate a unique client ID
        client_id = str(uuid.uuid4())

        # Login to the game promo API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                '(link unavailable)',
                json={'appToken': app_token, 'clientId': client_id, 'clientOrigin': 'deviceid'}
            )
            response.raise_for_status()
            client_token = response.json()['clientToken']

        # Emulate progress and generate a key
        async with httpx.AsyncClient() as client:
            response = await client.post(
                '(link unavailable)',
                headers={'Authorization': f'Bearer {client_token}'},
                json={'promoId': promo_id}
            )
            response.raise_for_status()
            key = response.json()['promoCode']

        print(f'Game: {game_name} | Key: {key}')

async def main():
    games = {
        1: {'name': 'Riding Extreme 3D', 'appToken': 'd28721be-fd2d-4b45-869e-9f253b554e50', 'promoId': '43e35910-c168-4634-ad4f-52fd764a843f'},
        2: {'name': 'Chain Cube 2048', 'appToken': 'd1690a07-3780-4068-810f-9b5bbf2931b2', 'promoId': 'b4170868-cef0-424f-8eb9-be0622e8e8e3'},
        3: {'name': 'My Clone Army', 'appToken': '74ee0b5b-775e-4bee-974f-63e7f4d5bacb', 'promoId': 'fe693b26-b342-4159-8808-15e3ff7f8767'},
        4: {'name': 'Train Miner', 'appToken': '82647f43-3f87-402d-88dd-09a90025313f', 'promoId': 'c4480ac7-e178-4973-8061-9ed5b2e17954'},
    }
    await generate_keys(games)

asyncio.run(main())
