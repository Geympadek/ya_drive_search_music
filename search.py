import requests
from config import YA_CLIENT_ID
import utils

def check_token(token: str):
    headers = {
        "Authorization": token
    }
    response = requests.get(f"https://cloud-api.yandex.net/v1/disk/", headers=headers, )

    return response.ok

def get_entries(token: str, offset = 0, limit = 20) -> list[dict[str, str]]:
    headers = {
        "Authorization": token
    }
    params = {
        "limit": limit,
        "media_type": "audio",
        "offset": offset,
        "fields": "items.name,items.path"
    }

    response = requests.get(f"https://cloud-api.yandex.net/v1/disk/resources/files", headers= headers, params=params)
    return response.json()["items"]

def worst_index(lst: list) -> int:
    return min(range(len(lst)), key=lambda i: lst[i][0])

def get_best(token: str, query: str, number: int = 5) -> list[dict]:
    batch_size = 20

    best = []

    cursor = 0
    while True:
        entries = get_entries(token, cursor, batch_size)

        for entry in entries:
            name = entry["name"]
            simil = utils.similarity(query, name)
            
            if len(best) < number:
                if simil > 0.3:
                    best.append((simil, entry))
            else:
                best[worst_index(best)] = (simil, entry)

        if len(entries) < batch_size:
            break

        cursor += batch_size
    return [el[1] for el in best]

def gen_url(token: str, path_to_file: str) -> str:
    headers = {
        "Authorization": token
    }
    params = {
        "path": path_to_file,
        "fields": "href"
    }
    response = requests.get(f"https://cloud-api.yandex.net/v1/disk/resources/download", headers=headers, params=params)
    return response.json()["href"]