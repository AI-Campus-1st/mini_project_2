from ..client import fetch
from datetime import datetime

async def get_de_facto_population(client, sem,api_key, url, day, tt="00", code=""):
    # Actual request
    # Tried using header but kept returning 500 error.
    request_url = url + f'{api_key}/json/Spop250mLocalResdJachi/1/365/{day.strftime("%Y%m%d")}/{tt}/{code}'

    return await fetch(client, request_url, params={}, sem=sem)