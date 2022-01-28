# +++++ IILEX PROGRAMMING LANGUAGE ++++
# +++++ "EASY ASSEMBLY" ++++++

from command import Command

class Ilex:

    # +++++ THE LIST OF COMMANDS THE USER ENTERED +++++
    commands = list()

    # +++++ THE LIST OF COMMAND WE ARE WORKING WITH (fcommands -> final commands)+++++
    fcommands = list()

    # +++++ INDEX OF LIST WE ARE CURRENTLY EXECUTING +++++
    programcounter = 0

    # +++++ COMMANDS WE ALLOW TO BE RUN +++++
    valid_commands = [
        "LOADI",
        "STORE",
        "JMP",
        "HOLD",
        "#",
        "METHOD",
        "ERROR"
    ]

    # +++++ IF THE KEY OF THE COMMAND IS EQUAL TO ANY OF THOSE THE VALUE IS AUTOMATICALY CORRECT +++++
    value_exceptions = [
        "METHOD",
        "HOLD",
        "JMP"
    ]

    # +++++ METHOD NAMES THE USER DECLARED +++++
    method_names = list()

    # +++++ EMPTY CONSTRUCTOR +++++
    def __init__(self):
        pass

    # +++++ INITIAL COMMANDS AND VARIABLES +++++
    def init_commands(self, commands):
        self.commands = commands
        self.check_valid()
        self.method_names = self.get_method_names()
        self.fcommands = self.sort_commands(0, list())
        #print(self.return_commands_readable(self.fcommands))
        #print(self.return_commands_readable(self.fcommands))

    # +++++ RETURN COMMANDS IN A READABLE FORMAT {('KEY', 'VALUE')} +++++
    def return_commands_readable(self, commands):
        return list(command.get() for command in commands)

    
    def get_method_names(self):
        method_names = list()
        for command in self.commands:
            if command.get_key() == "METHOD":
                method_names.append(command.get_value()[:-1])
        
        return method_names


    def index_of_method(self, method_name):
        index = 0
        for command in self.commands:
            if command.get_key() == "METHOD" and command.get_value() == method_name + ":":
                return index
            index += 1

    # +++++ CONVERT INPUT TO LIST FULL OF COMMANDS +++++
    def convert_list_to_commands(self, lst):
        res_lst = list()
        
        if len(lst) < 4:
            res_lst.append(Command("ERROR", "403"))
            return res_lst

        i = 0
        while i < len(lst):
            if ":" in lst[i]:
                res_lst.append(Command("METHOD", lst[i]))
                i += 1
            elif "HOLD" in lst[i]:
                res_lst.append(Command(lst[i], "END"))
                i += 1
            elif "#" in lst[i]:
                while i < len(lst):
                    i += 1
                    if "#" in lst[i]:
                        i += 1
                        break 
            else:
                try:
                    res_lst.append(Command(lst[i], lst[i+1]))        
                    i += 2
                except IndexError:
                    res_lst.append(Command("ERROR", "402"))
                    return res_lst

        return res_lst

    # +++++ CHECK IF EVERY INPUT WAS VALID +++++ 
    def check_valid(self):
        assert len(self.valid_commands) == 7, "Vergessen check_valid zu updaten"
        amount_of_valid_values = 0
        amount_of_valid_commands = 0
        amount_of_holds = 0

        for command in self.commands:

            if command.get_key() == "HOLD":
                amount_of_holds += 1

            if command.get_key() in self.value_exceptions:
                amount_of_valid_values += 1

            if command.get_key() in self.valid_commands:
                amount_of_valid_commands += 1

            if command.get_value().isnumeric():
                amount_of_valid_values += 1

        if amount_of_valid_commands < len(self.commands):
            self.commands.append(Command("Error", "402"))
            return False

        if amount_of_valid_values < len(self.commands):
            self.commands.append(Command("Error", "400"))
            return False

        if amount_of_holds is 0:
            self.commands.append(Command("Error", "401"))
            return False

        return True

    # +++++ SORT THE COMMANDS THE WAY THEY SHOULD BE EXECUTED +++++
    def sort_commands(self, start_index, res_lst):
        print(self.return_commands_readable(res_lst))
        if start_index >= len(self.commands) -1 or self.commands[start_index].get_value() is "HOLD":
            return res_lst

        if self.commands[start_index].get_key() == "JMP":
            called_method = self.commands[start_index].get_value()
            if called_method not in self.method_names:
                res_lst.append(Command("ERROR", "404"))
                return res_lst
        
            res_lst.append(self.commands[start_index])
            start_index = self.index_of_method(called_method)
            self.sort_commands(start_index, res_lst)

        elif self.commands[start_index].get_key() == "METHOD":
            self.sort_commands(start_index +1, res_lst)

        else:
            res_lst.append(self.commands[start_index])
            self.sort_commands(start_index+1, res_lst)



