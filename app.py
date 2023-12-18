from requests import get, Response
from os import getenv
from json import dumps
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from http.server import HTTPServer

class WebRequestHandler(BaseHTTPRequestHandler):
    service_url:str =  getenv("SERVICE_URL", "https://api.dictionaryapi.dev/api/v2/entries/en")
    debug:bool = getenv("DEBUG", "true") == "true"
    
    def safe_list_get(self, stuff:list) -> dict:
        """ Safely extract a list """
        if len(stuff) > 0:
            return stuff[0]
        return {}
    
    def get_single_meaning(self, response:Response) -> str:
        """ Extract the first definition from the dictionary service """
        meaning:str = self.safe_list_get(self.safe_list_get(self.safe_list_get(response.json()).get("meanings", [])).get("definitions", [])).get("definition", "")
        return dumps({ "meaning": meaning }).encode("utf-8")

    def get_response(self) -> str:
        """ Call dictionary service and get definitions """
        word:str = self.path[1:]
        endpoint = f"{self.service_url}/{word}"
        if self.debug:
            print(f"calling endpoint: {endpoint}")
        response:Response = get(endpoint)
        # return self.get_single_meaning(response)
        return dumps(response.json()).encode("utf-8")

    def do_GET(self):
        """ Override GET """
        resp = self.get_response()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(resp)

if __name__ == "__main__":
    port:int = int(getenv("PORT", "8080"))
    server:HTTPServer = HTTPServer(("0.0.0.0", port), WebRequestHandler)
    server.serve_forever()
