CREDENTIALS_MODEL_LOGIN = 'login'
CREDENTIALS_MODEL_EMAIL = 'email'
CREDENTIALS_MODEL_DOMAIN = 'domain'
CREDENTIALS_MODEL_PASSWORD = 'password'


class CredentialModel:
    def __init__(self, login: str, email: str, domain: str, password: str):
        self.login = login
        self.email = email
        self.domain = domain
        self.password = password

    def serialize(self) -> dict:
        return {
            CREDENTIALS_MODEL_LOGIN: self.login,
            CREDENTIALS_MODEL_EMAIL: self.email,
            CREDENTIALS_MODEL_DOMAIN: self.domain,
            CREDENTIALS_MODEL_PASSWORD: self.password,
        }

    @staticmethod
    def deserialize(payload):
        login = payload[CREDENTIALS_MODEL_LOGIN]
        email = payload[CREDENTIALS_MODEL_EMAIL]
        domain = payload[CREDENTIALS_MODEL_DOMAIN]
        password = payload[CREDENTIALS_MODEL_PASSWORD]
        return CredentialModel(login, email, domain, password)

