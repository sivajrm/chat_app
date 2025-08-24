from ChatDriver import ChatDriver

if __name__ == "__main__":
    chat_driver = ChatDriver()
    chat_driver.init_setup()
    topic = input("Enter topic of interest: ")
    chat_driver.start_chat(topic)
