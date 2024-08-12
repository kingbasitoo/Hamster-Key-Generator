# Games Key Generator

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

client_id = "https://api.gamepromo.io/promo/login-client"

def generate_keys():
    keys = {}
    for game_id, game_info in games.items():
        keys[game_info['name']] = {
            'appToken': game_info['appToken'],
            'promoId': game_info['promoId'],
            'client_id': client_id
        }
    return keys

if __name__ == "__main__":
    generated_keys = generate_keys()
    for game, info in generated_keys.items():
        print(f"Game: {game}, App Token: {info['appToken']}, Promo ID: {info['promoId']}, Client ID: {info['client_id']}")
