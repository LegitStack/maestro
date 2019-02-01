class MSGBoard():
    def __init__(self, name):
        self.name = name
        self.id = 1
        self.messages = [{'id': 0, 'ref_id': 0, 'request': '', 'response': 'initial'}]

    def add_message(self, message):
        message, answer = self.validate_message(message)
        if answer:
            self.messages.append(message)
            return True
        return False

    def get_message(self, reverse_index=1):
        return self.messages[reverse_index * -1]

    def get_messages(self, count=2, start_at=None):
        if not start_at:
            return self.messages[count * -1:]
        else:
            return self.messages[start_at:start_at + count]

    def validate_message(self, message):
        '''
        here's what I'm thinking about the protocol:
        a message is a dictionary of values
        a message requires an ID which is a huge random number.
        if a message ID is not included the message board will put one on.
        if a message contains REF_ID it is a response to a request and requires RESPONSE
        if a message contains FUNCTION it is a request that someone run the request listed as it's value.
        '''
        if 'id' not in message.keys():
            message['id'] = self.produce_id()
        if 'ref_id' in message.keys() and 'response' in message.keys():
            return message, True
        if 'request' in message.keys():
            return message, True
        return message, False

    def produce_id(self):
        self.id += 1
        return self.id - 1  # len(self.messages)
