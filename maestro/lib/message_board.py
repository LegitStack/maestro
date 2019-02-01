''' msgboard is for coolaboration and consensus '''

class MSGBoard():
    def __init__(self):
        self.id = 1
        self.messages = []

    def add_message(self, message: dict) -> bool:
        message, answer = self.validate_message(message=message)
        if answer:
            self.messages.append(message)
            return True
        return False

    def get_message(self, reverse_index: int = 1) -> list:
        return self.messages[reverse_index * -1:]

    def get_messages(self, count=2, start_at=None):
            if not start_at:
                return self.messages[count * -1:]
            else:
                return self.messages[start_at:start_at + count]

    def clear_messages(self) -> bool:
        self.id = 1
        self.messages = []
        return True

    def validate_message(self, message: dict) -> (dict, bool):
        ''' a message is a dictionary of values '''
        if 'id' not in message.keys():
            message['id'] = self.produce_id()
        return message, False

    def produce_id(self) -> int:
        self.id += 1
        return self.id - 1
