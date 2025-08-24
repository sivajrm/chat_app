COMM_SERVICES = {}

def register_service(name: str):

    def wrapper(cls):
        COMM_SERVICES[name] = cls
        return cls
    return wrapper
