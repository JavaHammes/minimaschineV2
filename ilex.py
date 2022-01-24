# +++++ IILEX PROGRAMMING LANGUAGE ++++
# +++++ "EASY ASSEMBLY" ++++++

from operator import truediv
from command import Command

class Ilex:

    commands = list()

    valid_commands = (
        "LOADI",
        "STORE",
        "JMP",
        "HOLD",
        "#",
        "METHOD",
        "ERROR"
    )

    def __init__(self):
        pass

    def init_commands(self, commands):
        self.commands = commands

    def return_commands_readable(self):
        return list(command.get() for command in self.commands)

    def convert_list_to_commands(self, lst):
        res_lst = list()
        
        if len(lst) < 2:
            res_lst.append(Command("ERROR", "403"))
            return res_lst

        i = 0
        while i < len(lst):
            if ":" in lst[i]:
                res_lst.append(Command("METHOD", lst[i]))
                i += 1
            elif "HOLD" in lst[i]:
                res_lst.append(Command(lst[i], "END"))
                if i is not len(lst)-1:
                    res_lst.append(Command("ERROR", "404"))
                return res_lst
            elif "#" in lst[i]:
                while i < len(lst):
                    i += 1
                    if "#" in lst[i]:
                        i += 1
                        break
            else:
                res_lst.append(Command(lst[i], lst[i+1]))        
                i += 2
        
        return res_lst

    def check_valid(self):
        amount_of_valid_commands = 0
        for command in self.commands:
            for valid_command in self.valid_commands:
                if command.get_key() == valid_command:
                    amount_of_valid_commands += 1
                    continue
        
        return (amount_of_valid_commands is len(self.commands))


