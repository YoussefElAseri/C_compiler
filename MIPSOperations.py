import struct
from Nodes import *


class Register:
    register = 0
    type = None
    # address is only for variables and arrays, needed so ++ and -- can manipulate actual value
    # index
    arrayAddress = None
    # juiste plaats
    pointerAddress = None
    arraySize = None

    def assign(self, register_nr, type1):
        self.register = register_nr
        self.type = type1

    def save(self, value, register_nr=0):
        if isinstance(value, str) and len(value) == 1:
            value = "\'" + value + "\'"

        if self.type == "f":
            return f"li $t{register_nr}, {value}\n" \
                   f"mtc1 $t{register_nr}, $f{self.register}"
        elif self.type == "s":
            return f"li $s{self.register}, {value}"
        else:
            return f"li $t{self.register}, {value}"

    def load(self, register_nr=0):
        if self.type == "f":
            return f"mfc1 $t{register_nr}, {self}" \
                   f"l.s {self}, 0($t{register_nr})", self
        return f"lw {self}, 0({self})", self

    def __repr__(self):
        return f"${self.type}{self.register}"


class Local(Register):
    def __init__(self, offset, type):
        self.offset = offset
        self.type = type

    def loadLocal(self, register_nr, offset):
        newRegister = Register()
        if self.type == "float":
            newType = "f"
            instruction = f"l.s $f{register_nr}, {offset - self.offset}($sp)"
        elif self.type == "byte":
            newType = "t"
            instruction = f"lb $t{register_nr}, {offset - self.offset}($sp)"
        else:
            newType = "t"
            instruction = f"lw $t{register_nr}, {offset - self.offset}($sp)"

        newRegister.assign(register_nr, newType)
        return instruction, newRegister

    def storeLocal(self, register, offset):
        if self.type == "float":
            return f"s.s {register}, {offset - self.offset}($sp)"
        else:
            return f"sw {register}, {offset - self.offset}($sp)"

    def loadAddress(self, register_nr, offset):
        newRegister = Register()
        instruction = f"addi $t{register_nr}, $sp, {offset - self.offset}"

        newRegister.assign(register_nr, "t")
        return instruction, newRegister


class Global(Register):
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def loadGlobal(self, register_nr):
        newRegister = Register()
        if self.type == "float":
            newType = "f"
            instruction = f"l.s $f{register_nr}, {self.name}"
        elif self.type == "byte":
            newType = "t"
            instruction = f"lb $t{register_nr}, {self.name}"
        else:
            newType = "t"
            instruction = f"lw $t{register_nr}, {self.name}"

        newRegister.assign(register_nr, newType)
        return instruction, newRegister

    def storeGlobal(self, register):
        if self.type == "float":
            return f"s.s {register}, {self.name}"
        else:
            return f"sw {register}, {self.name}"

    def loadAdress(self, register_nr):
        newRegister = Register()
        instruction = f"la $t{register_nr}, {self.name}"
        newRegister.assign(register_nr, "t")
        return instruction, newRegister


class GlobalArray(Register):
    def __init__(self, name, type, size, arraySize):
        self.name = name
        self.type = type
        self.size = size
        self.arraySize = arraySize

    def loadGlobal(self, register_nr, index):
        newRegister = Register()
        if self.type == "float":
            newType = "f"
            instruction = f"l.s $f{register_nr}, {index}({self.name})"
        elif self.type == "byte":
            newType = "t"
            instruction = f"lb $t{register_nr}, {index}({self.name})"
        else:
            newType = "t"
            instruction = f"lw $t{register_nr}, {index}({self.name})"

        newRegister.assign(register_nr, newType)
        return instruction, newRegister

    def loadAddress(self, register_nr):
        return f"la $t{register_nr}, {self.name}"


class LocalArray(Register):
    def __init__(self, offset, type, size, arraySize):
        self.offset = offset
        self.type = type
        # size is 1 or 4 (byte or int/float)
        self.size = size
        self.arraySize = arraySize

    def loadLocal(self, register_nr, index):
        newRegister = Register()
        if self.type == "float":
            newType = "f"
            instruction = f"l.s $f{register_nr}, ({index})"
        elif self.type == "byte":
            newType = "t"
            instruction = f"lb $t{register_nr}, ({index})"
        else:
            newType = "t"
            instruction = f"lw $t{register_nr}, ({index})"

        newRegister.assign(register_nr, newType)
        return instruction, newRegister


# Parse a string for Printf
def parse_string(string: str, argument: list[ArgumentNode]) -> list:
    if not argument:
        return ["\"" + string + "\""]
    parsed_parts: list = []
    index: int = 0  # Index to parsed_parts
    arg_ctr: int = 0

    for i in range(0, len(string)):
        if string[i - 1] == "%":
            continue
        if string[i] == "%":
            a = argument[arg_ctr].value
            if isinstance(a, str):
                if not parsed_parts or not isinstance(parsed_parts[-1], str):
                    parsed_parts.append(a[1:-1])
                else:
                    parsed_parts[-1] += a[1:-1]
            else:
                parsed_parts.append([string[i + 1:i + 2], a])
            arg_ctr += 1
        else:
            if not parsed_parts or not isinstance(parsed_parts[-1], str):
                parsed_parts.append(string[i])
                index += 1
            else:
                parsed_parts[-1] += string[i]

    for i in range(0, len(parsed_parts)):
        if isinstance(parsed_parts[i], str):
            parsed_parts[i] = "\"" + parsed_parts[i] + "\""

    return parsed_parts


def parse_string2(string: str, argument: list[ArgumentNode]) -> list:
    # parsed: str = "\""
    # vars: list = []
    parsed_parts: list = ["\""]
    index: int = 0  # Index to parsed_parts
    arg_ctr: int = 0
    for i in range(0, len(string)):
        if string[i - 1] == "%":
            continue
        if string[i] == "%":
            a = argument[arg_ctr].value
            if isinstance(a, str):
                parsed_parts[index] += a
            elif a.type == "literal":
                parsed_parts[index] += a.value
            elif a.type == "variable":
                # parsed += '%'
                parsed_parts[index] += "\""
                parsed_parts.append("%" + string[i + 1] + a.name)  # string i+1 = d,s
                index += 2
                parsed_parts.append("\"")
            else:
                print("errorElse")
            arg_ctr += 1
        else:
            parsed_parts[index] += string[i]

    if parsed_parts[index][0] != "%":
        parsed_parts[index] += "\""
    parsed_parts2: list = []
    for i in parsed_parts:
        if i != "\"\"":
            parsed_parts2.append(i)
    return parsed_parts2


def compile_scanf_string(string: str) -> list[str]:
    string.replace(" ", "")
    if string[-2:] == "\n":
        string = string[:-2]

    list: list = []
    for i in range(0, len(string)):
        if string[i] == "%":
            if string[i + 1].isnumeric():
                nr: str = string[i + 1: i + 2]
                list.append("s" + nr)
            else:
                list.append(string[i + 1:i + 2])

    return list


def float_to_hex(f):
    # Pack the float value into a 4-byte string using the 'f' format specifier
    packed = struct.pack('f', f)

    # Unpack the packed bytes as an unsigned integer in little-endian byte order
    # and format it as a 32-bit hexadecimal string
    hex_str = hex(struct.unpack('<I', packed)[0])

    # Return the hexadecimal string
    return hex_str


def add(dest, src1, src2):
    if dest.type == "f":
        return f"add.s {dest}, {src1}, {src2}"
    elif dest.type == "s":
        return f"add {dest}, {src1}, {src2}"
    else:
        return f"addu {dest}, {src1}, {src2}"


def sub(dest, src1, src2):
    if dest.type == "f":
        return f"sub.s {dest}, {src1}, {src2}"
    elif dest.type == "s":
        return f"sub {dest}, {src1}, {src2}"
    else:
        return f"subu {dest}, {src1}, {src2}"


def addi(dest, src, immediate):
    if dest.type == "f":
        raise ValueError("Cannot perform addi operation on floating-point register")
    elif dest.type == "s":
        return f"addi {dest}, {src}, {immediate}"
    else:
        return f"addiu {dest}, {src}, {immediate}"


def subi(dest, src, immediate):
    if dest.type == "f":
        raise ValueError("Cannot perform subi operation on floating-point register")
    elif dest.type == "s":
        return f"subi {dest}, {src}, {immediate}"
    else:
        return f"subiu {dest}, {src}, {immediate}"


def convert_float_to_int(dest, src):
    return f"cvt.w.s {dest}, {src}"


def convert_int_to_float(dest, src):
    return f"cvt.s.w {dest}, {src}"


def neg(dest, src):
    if dest.type == "f":
        return f"neg.s {dest}, {src}"
    else:
        return f"neg {dest}, {src}"


def logical_not(dest, src):
    return f"xori {dest}, {src}, 1"


def multiply(dest, src1, src2):
    if dest.type == "f":
        return f"mul.s {dest}, {src1}, {src2}"
    else:  # Assuming data_type is "int"
        return f"mul {dest}, {src1}, {src2}"


def divide(dest, src1, src2):
    if dest.type == "f":
        return f"div.s {dest}, {src1}, {src2}"
    else:  # Assuming data_type is "int"
        return f"div {dest}, {src1}, {src2}"


def modulo(dest, src1, src2):
    if dest.type == "f":
        return f"rem.s {src1}, {src2}\n" \
               f"mov.s {dest}, {src1}"
    else:  # Assuming data_type is "int"
        return f"div {src1}, {src2}\n" \
               f"mfhi {dest}"


# assuming one is stored in temp
def compare(dest, op, src1, src2, temp=None):
    if dest.type == "f":
        instruction = ""
        if op == "<":
            instruction = f"c.lt.s {src1}, {src2}\n" \
                          f"movf {temp}, $zero"
        elif op == ">":
            instruction = f"c.lt.s {src2}, {src1}\n" \
                          f"movf {temp}, $zero"
        elif op == "<=":
            instruction = f"c.le.s {src1}, {src2}\n" \
                          f"movf {temp}, $zero"
        elif op == ">=":
            instruction = f"c.le.s {src2}, {src1}\n" \
                          f"movf {temp}, $zero"
        elif op == "==":
            instruction = f"c.eq.s {src1}, {src2}\n" \
                          f"movf {temp}, $zero"
        elif op == "!=":
            instruction = f"c.eq.s {src1}, {src2}\n" \
                          f"movt {temp}, $zero"
        else:
            raise ValueError("Invalid comparison operator")
        instruction += f"\nmtc1 {temp}, {src1}"
        return instruction
    else:
        if op == "<":
            return f"slt {dest}, {src1}, {src2}"
        elif op == ">":
            return f"slt {dest}, {src2}, {src1}"
        elif op == "<=":
            return f"slt {dest}, {src2}, {src1}\n" \
                   f"xori {dest}, {dest}, 1"
        elif op == ">=":
            return f"slt {dest}, {src1}, {src2}\n" \
                   f"xori {dest}, {dest}, 1"
        elif op == "==":
            return f"seq {dest}, {src1}, {src2}"
        elif op == "!=":
            return f"sne {dest}, {src1}, {src2}"
        else:
            raise ValueError("Invalid comparison operator")


# no flaots
def logical_and(dest, src1, src2):
    return f"and {dest}, {src1}, {src2}"


# no floats
def logical_or(dest, src1, src2):
    return f"or {dest}, {src1}, {src2}"
