

class LLMServiceProvider:

    def __init__(self, id, name, api_url, api_key, auth_token, retries):
        self.id = id
        self.name = name
        self.api_url = api_url
        self.api_key = api_key
        self.auth_token = auth_token
        self.retries = retries