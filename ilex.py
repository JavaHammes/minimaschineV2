# +++++ IILEX PROGRAMMING LANGUAGE ++++
# +++++ "EASY ASSEMBLY" ++++++

from command import Command
from errors import Error
import time

class Ilex:

    # +++++ THE LIST OF COMMANDS THE USER ENTERED +++++
    commands = list()

    # +++++ LIST CONTAINING EVERY ERROR IN USERS PROGRAM +++++
    errors = list()

    # ++++ RETURN VALUES +++++
    akkumulator = 0
    befehlsregister_key = ""
    befehlsregister_value = ""
    programmzähler = 0

    regs = [
        0000000000000000,
        0000000000000000,
        0000000000000000,
        0000000000000000,
        0000000000000000,
        0000000000000000,
        0000000000000000,
        0000000000000000,
    ]

    ov = 0
    zr = 0
    sf = 0
    pf = 0

    # +++++ COMMANDS WE ALLOW TO BE RUN +++++
    valid_commands = [
        "#",
        "METHOD",
        "LOADI",
        "LOAD",
        "STORE",
        "ADD",
        "SUB",
        "MUL",
        "DIV",
        "MOD",
        "CMP",
        "ADDI",
        "SUBI",
        "MULI",
        "DIVI",
        "MODI",
        "CMPI",
        "AND",
        "OR",
        "XOR",
        "NOT",
        "SHL",
        "SHR",
        "ANDI",
        "ORI",
        "XORI",
        "SHLI",
        "SHRI",
        "JMPP",
        "JMPNN",
        "JMPN",
        "JMPNP",
        "JMPZ",
        "JMPV",
        "JMP",
        "JGT",
        "JGE",
        "JLT",
        "JLE",
        "JEQ",
        "JNE",
        "JOV",
        "HOLD",
        "NOOP"
    ]

    # +++++ IF THE KEY OF THE COMMAND IS EQUAL TO ANY OF THOSE, THE VALUE IS AUTOMATICLY CORRECT +++++
    value_exceptions = [
        "METHOD",
        "HOLD",
        "NOOP",
        "JMPP",
        "JMPNN",
        "JMPN",
        "JMPNP",
        "JMPZ",
        "JMPNZ",
        "JMPV",
        "JMP",
        "JGT",
        "JGE",
        "JLT",
        "JLE",
        "JEQ",
        "JNE",
        "JOV",
        "NOT"
    ]

    # +++++ METHODNAMES THE USER DECLARED +++++
    method_names = list()

    # +++++ EMPTY CONSTRUCTOR +++++
    def __init__(self):
        pass

    # +++++ INITIAL COMMANDS AND VARIABLES +++++
    def init_commands(self, commands, single):
        if not single:
            self.set_every_value(0)
            self.commands = commands
            self.check_valid()
            self.method_names = self.get_method_names()
        else:
            self.commands = commands
            self.check_valid()
            self.method_names = self.get_method_names()

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

    # +++++ RETURN INDEX OF METHODNAME +++++
    def index_of_method(self, method_name):
        index = 0
        for command in self.commands:
            if command.get_key() == "METHOD" and command.get_value() == method_name + ":":
                return index
            index += 1

    # +++++ CONVERT INTEGER TO 16 LONG BIT-NUMBER +++++
    def convert_to_bin16(self, integer):
        if integer >= 0:
            return "0" + "0" * (15-len(bin(integer))+2) + str(bin(integer)[2:])
        else:
            return "1" + "0" * (15 - len(bin(integer)) +2) + str(bin(integer)[3:])

    # +++++ CONVERT 16 LONG BIT-NUMBER TO INTEGER +++++
    def convert_bin16_int(self, bin16):
        if str(bin16)[0] == "0":
            try:
                return int(str(bin16)[str(bin16).find("1"):], 2)
            except ValueError:
                return bin16
        else:
            try:
                bin16_pos = str(bin16)[1:]
                return -int(bin16_pos[bin16_pos.find("1"):], 2)
            except Exception:
                return bin16

    # +++++ CONVERT INPUT TO LIST FULL OF COMMANDS [Command, Command, Command...]+++++
    def convert_list_to_commands(self, lst):
        res_lst = list()
        
        if len(lst) < 4:
            self.errors.append(Error(403))
            return res_lst

        i = 0
        while i < len(lst):
            if ":" in lst[i]:
                res_lst.append(Command("METHOD", lst[i]))
                i += 1
            elif "HOLD" in lst[i]:
                res_lst.append(Command(lst[i], "END"))
                i += 1
            elif "NOOP" in lst[i]:
                res_lst.append(Command(lst[i],"NOOP"))
                i += 1
            elif "NOT" in lst[i]:
                res_lst.append(Command(lst[i],"NOT"))
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
                    self.errors.append(Error(402))
                    return res_lst

        return res_lst

    # +++++ CHECK IF EVERY INPUT WAS VALID +++++ 
    def check_valid(self):
        amount_of_valid_values = 0
        amount_of_valid_commands = 0

        for command in self.commands:

            if command.get_key() in self.value_exceptions:
                amount_of_valid_values += 1

            if command.get_key() in self.valid_commands:
                amount_of_valid_commands += 1

            if command.get_value().lstrip("-").isnumeric():
                amount_of_valid_values += 1

        if amount_of_valid_commands < len(self.commands):
            self.errors.append(Error(401))
            return False

        if amount_of_valid_values < len(self.commands):
            self.errors.append(Error(402))
            return False

        return True

    # +++++ RUN CODE +++++
    def run_code(self, single):
        if self.errors:
            self.errors.sort(key=Error.importance)
            self.set_every_value(self.errors[0].error_value)
            return
        if not single:
            while self.commands[self.programmzähler].get_key() != "HOLD":
                if self.errors:
                    self.errors.sort(key=Error.importance)
                    self.set_every_value(self.errors[0].error_value)
                    return
                if self.programmzähler >= len(self.commands) -1:
                    self.errors.append(Error(400))
                    self.set_every_value(400)
                    return 
                try:
                    self.execute_command(self.commands[self.programmzähler]);
                except AttributeError:
                    print(self.commands[self.programmzähler].get_key() + " method missing")
                    self.programmzähler += 1
        else:
            if self.commands[self.programmzähler].get_key() == "HOLD":
                return

            if self.programmzähler >= len(self.commands) -1:
                self.errors.append(Error(400))
                self.set_every_value(400)
                return 

            try:
                self.execute_command(self.commands[self.programmzähler]);
            except AttributeError:
                print(self.commands[self.programmzähler].get_key() + " method missing")
                self.programmzähler += 1

    # +++++ EXECUTE ONE SPECIFIC COMMAND +++++
    def execute_command(self, command):

        key = command.get_key()
        value = command.get_value()

        self.befehlsregister_key = key
        self.befehlsregister_value = value

        getattr(Ilex, key)(self, value)

        if key != "CMPI" and key != "CMP":
            self.set_flags()

    # +++++ METHOD TO SET EVERY VALUE TO ONE SPECIFIC VALUE +++++
    def set_every_value(self, value):
        self.akkumulator = value
        self.programmzähler = value

        if value == 0:
            self.befehlsregister_key = ""
            self.befehlsregister_value = ""
            self.reset_regs()
            self.reset_flags()
            self.errors = list()
        else:
            self.befehlsregister_key = str(value)
            self.befehlsregister_value = str(value)
            self.regs = [
                value,
                value,
                value,
                value,
                value,
                value,
                value,
                value,
            ]

            self.ov = value
            self.zr = value
            self.sf = value
            self.pf = value

    # +++++ RESET EVERY FLAG +++++
    def reset_flags(self):
        self.ov = 0
        self.zr = 0
        self.sf = 0
        self.pf = 0

    # +++++ RESET EVERY REGISTER +++++
    def reset_regs(self):
        self.regs = [
            0000000000000000,
            0000000000000000,
            0000000000000000,
            0000000000000000,
            0000000000000000,
            0000000000000000,
            0000000000000000,
            0000000000000000,
        ]        

    # +++++ 

    def set_flags(self):

        akku_value = int(self.akkumulator)

        if akku_value < 0:
            self.sf = 1
        else:
            self.sf = 0

        if akku_value == 0:
            self.zr = 1
        else:
            self.zr = 0
        
        if akku_value % 2 == 0:
            self.pf = 1
        else:
            self.pf = 0

        if akku_value > 32767:
            self.ov = 1
            self.akkumulator = 32767
        elif akku_value < -32767:
            self.ov = 1
            self.akkumulator = -32767
        else:
            self.ov = 0

    # +++++ ILEX METHODS +++++

    def LOAD(self, reg_num):
        self.akkumulator = self.convert_bin16_int(self.regs[int(reg_num)-1])
        self.programmzähler += 1

    def LOADI(self, number):
        self.akkumulator = number
        self.programmzähler += 1

    def STORE(self, reg_num):
        self.regs[int(reg_num)-1] = self.convert_to_bin16(int(self.akkumulator))
        self.programmzähler += 1

    def ADD(self, reg_num):
        self.akkumulator = int(self.akkumulator) + int(self.convert_bin16_int(self.regs[int(reg_num)-1]))
        self.programmzähler += 1

    def SUB(self, reg_num):
        self.akkumulator = int(self.akkumulator) - int(self.convert_bin16_int(self.regs[int(reg_num)-1]))
        self.programmzähler += 1

    def MUL(self, reg_num):
        self.akkumulator = int(self.akkumulator) * int(self.convert_bin16_int(self.regs[int(reg_num)-1]))
        self.programmzähler += 1

    def DIV(self, reg_num):
        self.akkumulator = int(int(self.akkumulator) / int(self.convert_bin16_int(self.regs[int(reg_num)-1])))
        self.programmzähler += 1

    def MOD(self, reg_num):
        self.akkumulator = int(self.akkumulator) % int(self.convert_bin16_int(self.regs[int(reg_num)-1]))
        self.programmzähler += 1

    def CMP(self, reg_num):
        if self.akkumulator == str(self.convert_bin16_int(self.regs[int(reg_num)-1])):
            self.zr = 1
        else:
            self.zr = 0
        self.programmzähler += 1

    def ADDI(self, number):
        self.akkumulator = int(self.akkumulator) + int(number)
        self.programmzähler += 1

    def SUBI(self, number):
        self.akkumulator  = int(self.akkumulator) - int(number)
        self.programmzähler += 1

    def MULI(self, number):
        self.akkumulator = int(self.akkumulator) * int(number)
        self.programmzähler += 1

    def DIVI(self, number):
        self.akkumulator = int(int(self.akkumulator) / int(number))
        self.programmzähler += 1

    def MODI(self, number):
        self.akkumulator = int(self.akkumulator) % int(number)
        self.programmzähler += 1

    def CMPI(self, number):
        if self.akkumulator == number:
            self.zr = 1
        else:
            self.zr = 0
        self.programmzähler += 1

    def AND(self, reg_num):
        self.akkumulator = int(self.akkumulator) & int(self.convert_bin16_int(self.regs[int(reg_num)-1]))
        self.programmzähler += 1

    def OR(self, reg_num):
        self.akkumulator = int(self.akkumulator) | int(self.convert_bin16_int(self.regs[int(reg_num)-1]))
        self.programmzähler += 1

    def XOR(self, reg_num):
        self.akkumulator = int(self.akkumulator) ^ int(self.convert_bin16_int(self.regs[int(reg_num)-1]))
        self.programmzähler += 1   
    
    def NOT(self, NOT):
        self.akkumulator = ~int(self.akkumulator)
        self.programmzähler += 1

    def SHL(self, reg_num):
        self.akkumulator = int(self.akkumulator) << int(self.convert_bin16_int(self.regs[int(reg_num)-1]))
        self.programmzähler += 1

    def SHR(self, reg_num):
        self.akkumulator = int(self.akkumulator) >> int(self.convert_bin16_int(self.regs[int(reg_num)-1]))
        self.programmzähler += 1

    def ANDI(self, number):
        self.akkumulator = int(self.akkumulator) & int(number)
        self.programmzähler += 1

    def ORI(self, number):
        self.akkumulator = int(self.akkumulator) | int(number)
        self.programmzähler += 1

    def XORI(self, number):
        self.akkumulator = int(self.akkumulator) ^ int(number)
        self.programmzähler += 1  
    
    def NOTI(self, number):
        self.akkumulator = ~int(number)
        self.programmzähler += 1

    def SHLI(self, number):
        self.akkumulator = int(self.akkumulator) << int(number)
        self.programmzähler += 1

    def SHRI(self, number):
        self.akkumulator = int(self.akkumulator) >> int(number)
        self.programmzähler += 1

    def JMPP(self, method):
        if self.zr == 0 and self.sf == 0:
            self.JMP(method)
        else:
            self.programmzähler += 1

    def JMPNN(self, method):
        if self.sf == 0:
            self.JMP(method)
        else:
            self.programmzähler += 1

    def JMPN(self, method):
        if self.sf == 1:
            self.JMP(method)
        else:
            self.programmzähler += 1
            
    def JMPNP(self, method):
        if self.zr == 1 or self.sf == 1:
            self.JMP(method)
        else:
            self.programmzähler += 1

    def JMPZ(self, method):
        if self.zr == 1:
            self.JMP(method)
        else:
            self.programmzähler += 1

    def JMPNZ(self, method):
        if self.zr == 0:
            self.JMP(method)
        else:
            self.programmzähler += 1

    def JMPV(self, method):
        if self.ov == 1:
            self.JMP(method)
        else:
            self.programmzähler += 1

    def JMP(self, method):
        if method in self.method_names:
            self.programmzähler = self.index_of_method(method)+1
        else:
            self.errors.append(Error(404))
            self.programmzähler += 1

    def JGT(self, method):
        self.JMPP(method)

    def JGE(self, method):
        self.JMPNN(method)

    def JLT(self, method):
        self.JMPN(method)

    def JLE(self, method):
        self.JMNP(method)

    def JEQ(self, method):
        self.JMPZ(method)

    def JNE(self, method):
        self.JMPNZ(method)

    def JOV(self, method):
        self.JMPV(method)

    def NOOP(self, no_operation):
        time.sleep(0.01)
        self.programmzähler += 1

    def METHOD(self, value):
        self.programmzähler += 1



    # +++++ GET METHODS FOR APP.PY +++++
    def get_programmzähler(self):
        return self.programmzähler

    def get_akkumulator(self):
        return self.akkumulator
    
    def get_befehlsregister_key(self):
        return self.befehlsregister_key

    def get_befehlsregister_value(self):
        return self.befehlsregister_value

    def get_regs(self):
        return self.regs

    def get_ov(self):
        return self.ov

    def get_zr(self):
        return self.zr

    def get_sf(self):
        return self.sf

    def get_pf(self):
        return self.pf
