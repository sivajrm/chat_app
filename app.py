from ChatDriver import ChatDriver

if __name__ == "__main__":
    chat_driver = ChatDriver()
    chat_driver.init_setup()

    while True:
        print("Welcome to Chat App.... ")
        topic = input("I would like to explore about : ")
        chat_driver.start_chat(topic)
