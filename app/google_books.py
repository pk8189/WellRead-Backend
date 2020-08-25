import requests
from fastapi import HTTPException

BASE_URL = "https://www.googleapis.com/books/v1/volumes"


def query_google_books(query_string: str) -> list:
    res = requests.get(f"{BASE_URL}?q={query_string}&projection=full")
    if res.status_code == 200:
        results = res.json()["items"]
        if len(results) > 15:
            return results[:15]
        return results[: len(results)]
    raise HTTPException(
        status_code=res.status_code, detail=res.json()["error"]["message"]
    )


def get_google_book(volume_id: int) -> dict:
    res = requests.get(f"{BASE_URL}/{volume_id}")
    if res.status_code == 200:
        return res.json()
    raise HTTPException(
        status_code=res.status_code, detail=res.json()["error"]["message"]
    )
