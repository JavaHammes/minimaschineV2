class Command:

    command = ""
    value = ""

    def __init__(self, command, value):
        self.command = command
        self.value = value

    def get(self):
        return (self.command, self.value)

    def get_key(self):
        return self.command

    def get_value(self):
        return self.value