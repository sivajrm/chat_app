
import requests
import json
import textwrap
import re
from requests import Response

'''
    POST http://guanaco-submitter.guanaco-backend.k2.chaiverse.com/endpoints/onsite/chat

    Headers:
    Authorization Bearer CR_14d43f2bf78b4b0590c2a8b87f354746

    Body:
    {
        "memory": str,
        "prompt": str,
        "bot_name": str,
        "user_name": str,
        "chat_history": List[dict[str, str]]
    }

'''


def exchange_request(user_name, bot_name, prompt, chat_history) -> Response | None:
    url = "http://guanaco-submitter.guanaco-backend.k2.chaiverse.com/endpoints/onsite/chat"

    data = {
        "memory": "",
        "prompt": prompt,
        "bot_name": bot_name,
        "user_name": user_name,
        "chat_history": chat_history
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer CR_14d43f2bf78b4b0590c2a8b87f354746"
    }
    retries = 3
    while retries > 0:
        try:
            # Make the POST request
            response = requests.post(url, headers=headers, data=json.dumps(data))
            if response.headers.get("Transfer-Encoding") == "chunked":
                print("Have to wait here.... do not switch context")

            # Check the response
            if not (response.status_code == 200 or response.status_code == 201):
                print(f"Request failed with status {response.status_code} reason {response.text}")
                print("Retrying...")
                retries -= 1
            else:
                return response
        except requests.exceptions.RequestException as e:
            print("Error making POST request:", e)

    print("Internal error occurred, please try again later.")
    exit(0)

def add_to_history(input:list, sender, message):
    input.append({"sender": sender, "message": message})

def talk_to_chat_bot(bot_name, chat_history, prompt, user_name, text_color):
    response = exchange_request(user_name, bot_name, prompt, chat_history)
    model_reply = parse_response(response.text)
    model_reply = re.sub(r"\*.*?\*", "", model_reply).strip()

    print("\n")
    print("\033[" + text_color, bot_name, ": ")
    multi_line_replies = textwrap.wrap(model_reply, 60)
    for line in multi_line_replies:
        print(line)
    print("\033[0m")
    #add_to_history(chat_history, bot_name, model_reply)
    return model_reply


def parse_response(json_response):
    response_json = json.loads(json_response)
    return response_json.get("model_output")

def interact_with_chatbot(user_name, bot_name, topic):
    chat_history_bot1 = []
    chat_history_bot2 = []
    chat_history = []
    message = "Hello! How are you?, Do you know what's going on around " + topic
    #add_to_history(chat_history_bot1, "user", message)

    prompt = message
    first_time = True
    while True:
        if not first_time:
            add_to_history(chat_history_bot2, bot_name, message)
            prompt = talk_to_chat_bot(user_name, chat_history_bot2, message, bot_name, "32m")

        else:
            first_time = False
            print("\033[32m" + user_name + ":")
            print(message + "\033[0m")
            message += "\n You are a strict bot. Only respond with the person speaking. Do not include any narrative, actions, or descriptions"

        add_to_history(chat_history_bot1, user_name, prompt)
        add_to_history(chat_history, user_name, prompt)
        bot_message = talk_to_chat_bot(bot_name, chat_history_bot1, prompt, user_name, "34m")
        message = bot_message
        add_to_history(chat_history, bot_name, message)

if __name__ == "__main__":
    print("Enter user name")
    user_name = input()
    print("Enter bot name")
    bot_name = input()
    print("Enter topic of interest")
    topic = input()
    interact_with_chatbot(user_name, bot_name, topic)