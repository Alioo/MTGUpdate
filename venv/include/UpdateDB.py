import json
import psycopg2
import requests

def get_cards():
    Url = "https://api.scryfall.com/cards"
    req = requests.get(Url)
    conn = psycopg2.connect(database="magicdb", user="postgres", password="", host="127.0.0.1", port="5432")
    json_req = (req.json())
    while json_req['has_more']:
        for card in json_req['data']:
            oracle_id = card['oracle_id']
            scry_id = card['id']
            if 'image_uris' in card:
                image_uris = str(card['image_uris'])
            else:
                image_uris = ''
            if 'usd' in card:
                price = card['usd']
            else:
                price = '0.00'
            name = card['name']
            cur = conn.cursor()
            cur.execute("INSERT INTO Cards (name, image_uri, scry_id, id, price) VALUES (%s, %s, %s, %s, %s)"
                        "ON CONFLICT (id) DO UPDATE SET name = %s, image_uri = %s, scry_id = %s, "
                        "id = %s, price = %s", (name, image_uris, scry_id, oracle_id, price, name, image_uris, scry_id,
                                                oracle_id, price))
            conn.commit()

        req = requests.get(json_req['next_page'])
        json_req = (req.json())


get_cards()


