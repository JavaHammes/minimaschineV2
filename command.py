class Command:

    command = ""
    value = ""
    commands = list()

    def __init__(self, command, value):
        self.command = command
        self.value = value

    def get(self):
        return (self.command, self.value)

    def getCommand(self):
        return self.command

    def getValue(self):
        return self.value