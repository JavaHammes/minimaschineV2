# +++++ IILEX PROGRAMMING LANGUAGE ++++
# +++++ "EASY ASSEMBLY" ++++++

from command import Command

class Ilex:

    # +++++ THE LIST OF COMMANDS THE USER ENTERED +++++
    commands = list()

    # +++++ THE LIST OF COMMAND WE ARE WORKING WITH (fcommands -> final commands)+++++
    fcommands = list()

    # +++++ INDEX OF LIST WE ARE CURRENTLY EXECUTING +++++
    programzähler = 0

    # ++++ RETURN VALUES +++++
    akkumulator = 0
    befehlsregister_key = ""
    befehlsregister_value = 0

    reg_1 = 0000000000000000
    reg_2 = 0000000000000000
    reg_3 = 0000000000000000
    reg_4 = 0000000000000000
    reg_5 = 0000000000000000
    reg_6 = 0000000000000000
    reg_7 = 0000000000000000
    reg_8 = 0000000000000000

    ov = 0
    zr = 0
    sf = 0
    pf = 0

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
        # also declares fcommands inside the method
        self.sort_commands(0,list())
        print(self.return_commands_readable(self.fcommands))

    # +++++ RETURN COMMANDS IN A READABLE FORMAT {('KEY', 'VALUE')} +++++
    def return_commands_readable(self, commands):
        return list(command.get() for command in commands)

    # +++++ GET EVERY METHODS NAME WITHOUT ":" +++++
    def get_method_names(self):
        method_names = list()
        for command in self.commands:
            if command.get_key() == "METHOD":
                method_names.append(command.get_value()[:-1])
        
        return method_names

    # +++++ RETURN INDEX OF METHOD NAME +++++
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
        if start_index is None:
            res_lst.append(Command("ERROR", "404"))
            self.fcommands = res_lst
            return 

        if start_index >= len(self.commands) -1 or self.commands[start_index].get_value() == "HOLD":
            self.fcommands = res_lst
            return

        if self.commands[start_index].get_key() == "JMP":
            called_method = self.commands[start_index].get_value()
            if called_method not in self.method_names:
                res_lst.append(Command("ERROR", "404"))
                self.fcommands = res_lst
                return
        
            res_lst.append(self.commands[start_index])
            start_index = self.index_of_method(called_method)
            self.sort_commands(start_index, res_lst)

        elif self.commands[start_index].get_key() == "METHOD":
            self.sort_commands(start_index +1, res_lst)

        else:
            res_lst.append(self.commands[start_index])
            self.sort_commands(start_index+1, res_lst)


    # +++++ RUN CODE COMPLETLY +++++
    def run_code(self, single):
        if single is True:
            self.run_code_single()
            return

    # ++++++ RUN CODE STEP BY STEP +++++
    def run_code_single(self):
        pass

    # +++++ ILEX METHODS +++++
    def LOADI(self, number):
        self.akkumulator = number

    # +++++ GET METHODS FOR APP.PY +++++
    def get_programmzähler(self):
        return self.programzähler

    def get_akkumulator(self):
        return self.akkumulator
    
    def get_befehlsregister_key(self):
        return self.befehlsregister_key

    def get_befehlsregister_value(self):
        return self.befehlsregister_value

    def get_reg_1(self):
        return self.reg_1

    def get_reg_2(self):
        return self.reg_2

    def get_reg_2(self):
        return self.reg_2

    def get_reg_3(self):
        return self.reg_3

    def get_reg_4(self):
        return self.reg_4

    def get_reg_5(self):
        return self.reg_5

    def get_reg_6(self):
        return self.reg_6

    def get_reg_7(self):
        return self.reg_7

    def get_reg_8(self):
        return self.reg_8

    def get_ov(self):
        return self.ov

    def get_zr(self):
        return self.zr

    def get_sf(self):
        return self.sf

    def get_pf(self):
        return self.pf
