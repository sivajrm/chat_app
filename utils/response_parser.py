import re
import json

class ResponseParser:
    @staticmethod
    def parse(json_response):
        try:
            data = json.loads(json_response)
            return data.get("model_output", "")
        except json.JSONDecodeError:
            return ""

    @staticmethod
    def clean(text):
        # Remove narrative actions in *...*
        text = re.sub(r"\*.*?\*", "", text)
        return text.strip()
