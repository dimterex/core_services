import hashlib
from hashlib import sha256
from typing import Dict
from urllib import parse

from requests import Session


class KeeneticClient:

    def __init__(self, admin_endpoint: str, login: str, password: str):
        self._admin_endpoint = admin_endpoint
        self._login = login
        self._password = password
        self._session = None

    def logout(self):
        if self._session:
            self._session.close()
        self._session = None

    def login(self) -> bool:
        self._session = Session()
        auth_endpoint = f"{self._admin_endpoint}/auth"
        check_auth_response = self._session.get(auth_endpoint)
        if check_auth_response.status_code == 401:
            ndm_challenge = check_auth_response.headers.get('X-NDM-Challenge')
            ndm_realm = check_auth_response.headers.get('X-NDM-Realm')
            md5 = hashlib.md5((self._login + ':' + ndm_realm + ':' + self._password).encode('utf-8')).hexdigest()
            sha = sha256((ndm_challenge + md5).encode('utf-8')).hexdigest()
            auth_response = self._session.post(auth_endpoint, json={'login': self._login, 'password': sha})
            if auth_response.status_code == 200:
                return True
            else:
                raise ConnectionError(f"Keenetic authorisation failed. Status {auth_response.status_code}")
        elif check_auth_response.status_code == 200:
            return True
        raise ConnectionError(f"Failed to check authorisation, status unknown ({check_auth_response.status_code})")

    def metric(self, command: str, params: Dict) -> Dict:
        url = f"{self._admin_endpoint}/rci/show/{command.replace(' ', '/')}" + "?" + parse.urlencode(params)
        r = self._session.get(url)
        if r.status_code == 200:
            return r.json()
        raise Exception(r)

