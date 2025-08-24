


class ChatCommunicationService:

    def __init__(self, api_url, api_token, retries=3):
        self.api_url = api_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_token}"
        }
        self.retries = retries

    def send_message(self, user_name, bot_name, prompt, chat_history):



