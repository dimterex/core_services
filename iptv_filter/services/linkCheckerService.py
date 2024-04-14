import requests


class LinkCheckerService:
    def check(self, link: str):
        try:
            response = requests.head(link)
            return response.status_code == 200
        except:
            return False
