import time, requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
import httpx
import asyncio

def make_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
        logging.FileHandler("data/logs/crawler.log", encoding="utf-8"),
        logging.StreamHandler(),
        ],
    )
    return logging.getLogger('crawler')


async def fetch(client, url, params, sem):
    async with sem:
        r = await client.get(url, params=params)
        r.raise_for_status()
        return r.json()