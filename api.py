from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

token = "glpat-_pSLvL2QwXQzYuh7Krxy"
headers = {
        'Accepts': 'application/json',
        'Authorization': 'Bearer {}'.format(token),
        }

class Gitlab:
    def get_top_10(self):
        url = f"https://gitlab.com/api/v4/users/buddhitha/projects/"

        session = Session()
        session.headers.update(headers)

        response = session.get(url)
        data = json.loads(response.text)
        return data
    
    def create_project(self,name):
        parameters = {
            'name': {name},
            'visibility': 'private'
        }
        url = f"https://gitlab.com/api/v4/projects/"

        session = Session()
        session.headers.update(headers)

        response = session.post(url, params=parameters)
        data = json.loads(response.text)
        return data