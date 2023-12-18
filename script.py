from requests import get, Response
from os import getenv
from json import dumps
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from http.server import HTTPServer

service_url:str = getenv("SERVICE_URL", "https://api.dictionaryapi.dev/api/v2/entries/en")
debug:bool = getenv("DEBUG", "true") == "true"

def safe_list_get(stuff:list) -> dict:
    """ Safely extract a list """
    if len(stuff) > 0:
        return stuff[0]
    return {}

def get_single_meaning(response:Response) -> str:
    """ Extract the first definition from the dictionary service """
    meaning:str = safe_list_get(safe_list_get(safe_list_get(response.json()).get("meanings", [])).get("definitions", [])).get("definition", "")
    return dumps({ "meaning": meaning }).encode("utf-8")

def get_response(word) -> str:
    """ Call dictionary service and get definitions """
    endpoint = f"{service_url}/{word}"
    if debug:
        print(f"calling endpoint: {endpoint}")
    response:Response = get(endpoint)
    # return self.get_single_meaning(response)
    return dumps(response.json()).encode("utf-8")

if __name__ == "__main__":
    word:str = getenv("WORD", "linux")
    print(get_response(word))
