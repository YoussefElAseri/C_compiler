from Nodes import *
from AST import AST
from SymbolTable import SymbolTable
from MIPSOperations import *

class MIPSVisitor:
    def __init__(self):
        self.file = ""
        self.data = [".data"]
        self.text = [".text"]
        self.treg = 0
        self.freg = 0
        self.offset = 0

        self.fs: list[int] = []

        # Symbol Tables
        self.symbol_table: SymbolTable = SymbolTable([0])
        self.cur_symbol_table: SymbolTable = self.symbol_table

        # block labels
        self.blocks = []

        self.if_label: int = -1
        self.while_label: int = -1
        self.printf_label: int = -1
        self.scanf_label: int = -1
        self.main: bool = False
        self.functions: list[FuncDeclareNode] = []

    def visitRun(self, node: RunNode):
        if node.include:
            self.includeStdio()
        for child in node.children:
            child.generateMips(self)


        # write result to file
        file = open(self.file, "w")
        for data in self.data:
            file.write(data + '\n')
        for text in self.text:
            file.write(text + '\n')

        file.close()

    def increase_if_label(self) -> str:
        self.if_label = self.if_label + 1
        new_index: int = self.if_label
        return "ELSE_" + str(new_index)

    def increase_while_label(self) -> str:
        self.while_label = self.while_label + 1
        new_index: int = self.while_label
        return "WHILE_" + str(new_index)

    def increase_printf_label(self) -> str:
        self.printf_label = self.printf_label + 1
        new_index: int = self.printf_label
        return "printf_" + str(new_index)

    def increase_scanf_label(self) -> str:
        self.scanf_label = self.scanf_label + 1
        new_index: int = self.scanf_label
        return "scanf_" + str(new_index)

    def visitIf(self, node: IfNode):
        else_label = self.increase_if_label()
        end_label = "DONE_" + str(self.if_label)

        # First parse Node Condition
        condition = self.getValue(node.condition.generateMips(self))
        if condition.type == "f":
            newRegister = Register()
            newRegister.assign(self.treg, "t")
            self.treg += 1
            self.freg -= 1
            self.text.append(convert_float_to_int(newRegister, condition))
            condition = newRegister

        if node.elseNode:
            self.text.append(f"beqz {condition} {else_label}")
        else:
            self.text.append(f"beqz {condition} {end_label}")

        node.block.generateMips(self)

        self.text.append(f"j {end_label}\n")

        if node.elseNode:
            self.text.append(f"{else_label}: \n")
            node.elseNode.generateMips(self)

        self.text.append(f"{end_label}: \n")

        # free condition
        self.treg -= 1

    def visitWhile(self, node: WhileNode):
        # Start of While block
        while_label: str = self.increase_while_label()
        done_label: str = "WHILE_DONE_" + str(self.while_label)
        self.text.append(while_label + ": ")

        condition = self.getValue(node.condition.generateMips(self))

        self.text.append(f"beqz {condition}  {done_label}")


        # Parse While block
        node.block.generateMips(self)

        # At end of while block, jump back to begin of While
        self.text.append("j " + while_label)
        self.text.append(done_label + ":")

        self.treg -= 1


    def visitInstantiation(self, node: InstantiationNode, global_var):
        if global_var:
            variable = self.declareGlobal(node.name, node.varType)
        else:
            variable = self.declareLocal(node.varType)

        if type(node.name) != str:
            nn = node.name.getText()
        else:
            nn = node.name
        self.cur_symbol_table.add_symbol(nn, variable.type, False, variable)

        return variable

    def visitArrayInstantiation(self, node: ArrayInstantiationNode, global_var):
        if global_var:
            variable = self.declareGlobalArray(node.name, node.varType, node.size)
        else:
            variable = self.declareLocalArray(node.varType, node.size)

        if type(node.name) != str:
            nn = node.name.getText()
        else:
            nn = node.name
        self.cur_symbol_table.add_symbol(nn, variable.type, False, variable)

        return variable

    def declareGlobal(self, name, type):
        if type == "int" or type == "bool":
            type = "word"
        elif type == "char":
            type = "byte"
        elif "float" in type:
            type = "float"
        elif "*" in type:
            type = "word"
        else:
            print(f"error151 {type} ")
        self.data.append(f"{name}: .{type} 0")
        return Global(name, type)

    def declareGlobalArray(self, name, type, size):
        singleSize = 0
        if type == "int" or type == "bool":
            singleSize = 4
            type = "word"
        elif type == "char":
            singleSize = 4
            type = "byte"
        elif "float" in type:
            singleSize = 4
            type = "float"
        self.data.append(f"{name}: .space {size * singleSize}")
        return GlobalArray(name, type, singleSize, size)

    def declareLocal(self, type):
        size = 0
        if type == "int" or type == "bool":
            size = 4
            type = "word"
        elif type == "char":
            size = 4
            type = "byte"
        elif "float" in type:
            size = 4
            type = "float"
        elif "*" in type:
            size = 4
            type = "word"
        f = self.offset
        self.offset += 4
        self.text.append(f"addi $sp, $sp, -{size}")
        return Local(f, type)

    def declareLocalArray(self, type, size):
        singleSize = 0
        if type == "int" or type == "bool":
            singleSize = 4
            type = "word"
        elif type == "char":
            singleSize = 4
            type = "byte"
        elif "float" in type:
            singleSize = 4
            type = "float"
        f = self.offset
        self.offset += 4
        self.text.append(f"addi $sp, $sp, -{size * singleSize}")
        return LocalArray(f, type, singleSize, size)

    def visitVariable(self, node: VariableNode) -> Register:
        return self.cur_symbol_table.get_symbol(node.name)['reg']

    def getValue(self, variable: Register):
        if isinstance(variable, Global):
            pass
        elif isinstance(variable, Local):
            pass
        elif isinstance(variable, Register):
            return variable

        if variable.type == "float":
            register_nr = self.freg
            self.freg += 1
        elif variable.type == "word" or variable.type == "byte":
            register_nr = self.treg
            self.treg += 1
        else:
            print("error224 " + variable.type)

        if isinstance(variable, Global):
            temp = variable.loadGlobal(register_nr)
            self.text.append(temp[0])
            variable = temp[1]
        elif isinstance(variable, Local):
            temp = variable.loadLocal(register_nr, self.offset)
            self.text.append(temp[0])
            variable = temp[1]

        return variable

    def visitLiteral(self, node: LiteralNode):
        value = node.convertValType()
        nlt = str(node.literalType)
        register = Register()
        if nlt == "int":
            register.assign(self.treg, "t")
            self.treg += 1
            self.text.append(register.save(value))
        elif nlt == "float":
            register.assign(self.freg, "f")
            self.freg += 1
            self.text.append(register.save(float_to_hex(value)))
        elif nlt == "char":
            register.assign(self.treg, "t")
            self.treg += 1
            self.text.append(register.save(value))
        elif nlt == "bool":
            register.assign(self.treg, "t")
            self.treg += 1
            if value:
                self.text.append(register.save(1))
            else:
                self.text.append(register.save(0))
        return register

    def visitAssignment(self, node: AssignmentNode):
        variable = node.left.generateMips(self)

        # implicit conversion
        if node.right.type == "literal" and variable.type == "f":
            if node.right.literalType == "int":
                node.right.literalType = "float"

        result = self.getValue(node.right.generateMips(self))

        # conversion
        newRegister = Register()
        if variable.type != "float" and result.type == "f":
            newRegister.assign(self.freg, "t")
            self.treg += 1
            self.freg -= 1
            self.text.append(convert_float_to_int(newRegister, result))
            result = newRegister
        elif variable.type == "float" and result.type != "f":
            newRegister.assign(self.freg, "f")
            self.freg += 1
            if result.type == "t":
                self.treg -= 1
            self.text.append(convert_int_to_float(newRegister, result))
            result = newRegister

        if isinstance(variable, Local):
            self.text.append(variable.storeLocal(result, self.offset))
        elif isinstance(variable, Global):
            self.text.append(variable.storeGlobal(result))
        elif isinstance(variable, Register):
            if variable.pointerAddress:
                if variable.type == "float":
                    self.text.append(f"s.s {result}, ({variable.pointerAddress})")
                else:
                    self.text.append(f"sw {result}, ({variable.pointerAddress})")
            elif variable.arrayAddress:
                if variable.type == "float":
                    self.text.append(f"s.s {result}, ({variable.arrayAddress})")
                else:
                    self.text.append(f"sw {result}, ({variable.arrayAddress})")

    def visitLogic(self, node: LogicNode):
        lRegister = self.getValue(node.left.generateMips(self))
        rRegister = self.getValue(node.right.generateMips(self))
        temp = self.poorerConversion(lRegister, rRegister)
        lRegister = temp[0]
        rRegister = temp[1]
        instruction = ""
        if lRegister[1] == "f":
            self.text.append(f"mtf1 {tempRegister} {lRegister}")


        if node.operation == "&&":
            instruction = logical_and(lRegister, lRegister, rRegister)
        elif node.operation == "||":
            instruction = logical_or(lRegister, lRegister, rRegister)
        self.treg -= 1

        self.text.append(instruction)
        return lRegister

    def visitCompare(self, node: CompareNode):
        lRegister = self.getValue(node.left.generateMips(self))
        rRegister = self.getValue(node.right.generateMips(self))
        temp = self.richerConversion(lRegister, rRegister)
        lRegister = temp[0]
        rRegister = temp[1]
        instruction = ""
        tempRegister = Register()
        if lRegister.type == "f":
            tempRegister.assign(self.treg, "t")
            self.text.append(tempRegister.save(1))
        instruction = compare(lRegister, node.operation, lRegister, rRegister, tempRegister)
        self.text.append(instruction)
        if rRegister.type == "f":
            self.freg -= 1
        else:
            self.treg -= 1
        return lRegister

    def visitTerm(self, node: TermNode):
        lRegister = self.getValue(node.left.generateMips(self))
        rRegister = self.getValue(node.right.generateMips(self))
        temp = self.richerConversion(lRegister, rRegister)
        lRegister = temp[0]
        rRegister = temp[1]
        instruction = ""
        if rRegister.type == "f":
            self.freg -= 1
        else:
            self.treg -= 1
        if node.operation == "+":
            instruction = add(lRegister, lRegister, rRegister)
        elif node.operation == "-":
            instruction = sub(lRegister, lRegister, rRegister)
        result = temp[0]
        self.text.append(instruction)
        return result

    def visitFactor(self, node: FactorNode):
        lRegister = self.getValue(node.left.generateMips(self))
        rRegister = self.getValue(node.right.generateMips(self))
        temp = self.richerConversion(lRegister, rRegister)
        lRegister = temp[0]
        rRegister = temp[1]
        if rRegister.type == "f":
            self.freg -= 1
        else:
            self.treg -= 1
        instruction = ""
        if node.operation == "*":
            instruction = multiply(lRegister, lRegister, rRegister)
        elif node.operation == "/":
            instruction = divide(lRegister, lRegister, rRegister)
        elif node.operation == "%":
            instruction = modulo(lRegister, lRegister, rRegister)
        self.text.append(instruction)
        return lRegister

    def visitUnary(self, node: UnaryNode):
        register = node.variable.generateMips(self)
        if node.operation == "&":
            temp = None
            if isinstance(register, Local):
                temp = register.loadAddress(self.treg)
            elif isinstance(register, Global):
                temp = register.loadAdress(self.treg)
            self.treg += 1
            self.text.append(temp[0])
            return temp[1]
        elif node.operation == "*":
            temp = None
            index = Register()
            # highest t register
            index.assign(7, "t")
            if isinstance(register, Local):
                temp = register.loadLocal(register.register, self.offset)
                index.save(register.offset)
            elif isinstance(register, Global):
                temp = register.loadGlobal(register.register)
                self.text.append(register.loadAdress(index.register)[0])
            elif isinstance(register, Register):
                self.text.append(index.save(0))
                self.text.append(add(index, index, register))
                self.text.append(register.load(self.treg)[0])
                register.pointerAddress = index
                return register
            temp[1].pointerAddress = index
            self.text.append(temp[0])
            return temp[1]
        register = self.getValue(register)
        instruction = ""
        floatType = register.type == "f"
        register = self.getValue(register)
        if node.operation == "-":
            self.text.append(neg(register, register))
        elif node.operation == "!":
            if floatType:
                register.assign(self.treg, "t")
                self.treg += 1
                self.freg -= 1
                self.text.append(convert_float_to_int(register, register))
            self.text.append(logical_not(register, register))
        elif node.operation == "+":
            return register
        return register

    def visitTypeCast(self, node: TypeCastNode):
        register = self.getValue(node.variable.generateMips(self))
        cast = node.castTo
        newRegister = Register()
        if cast == "float" and register.type != "f":
            newRegister.assign(self.freg, "f")
            self.freg += 1
            if register.type == "t":
                self.treg -= 1
            elif register.type == "s":
                self.sreg -= 1
            instruction = convert_int_to_float(newRegister, register)
        elif cast != "float" and register.type == "f":
            newRegister.assign(self.treg, "t")
            self.freg -= 1
            self.treg += 1
            instruction = convert_float_to_int(newRegister, register)
        else:
            newRegister = register
            instruction = ""

        self.text.append(instruction)
        return newRegister

    def visitSpecialUnary(self, node: SpecialUnaryNode):
        variable = node.variable.generateMips(self)  # Variable mag niet dict zijn
        value = self.getValue(variable)
        instruction = None
        floatType = (value.type == "f")
        if node.operation == "++":
            if floatType:
                tempRegister = Register()
                tempRegister.assign(self.freg, "f")
                self.text.append(tempRegister.save(1, self.treg))
                instruction = add(value, value, tempRegister)
            else:
                instruction = addi(value, value, 1)
        elif node.operation == "--":
            if floatType:
                tempRegister = Register()
                tempRegister.assign(self.freg, "f")
                self.text.append(tempRegister.save(1, self.treg))
                instruction = sub(value, value, tempRegister)
            else:
                instruction = subi(value, value, 1)
        self.text.append(instruction)
        # store new value in variable
        if isinstance(variable, Global):
            self.text.append(variable.storeGlobal(value))
        elif isinstance(variable, Local):
            self.text.append(variable.storeLocal(value, self.offset))
        # pointer and array
        else:
            if variable.pointerAddress:
                if variable.type == "float":
                    self.text.append(f"s.s {value}, ({variable.pointerAddress})")
                else:
                    self.text.append(f"sw {value}, ({variable.pointerAddress})")
            elif variable.arrayAddress:
                if variable.type == "float":
                    self.text.append(f"s.s {value}, ({variable.arrayAddress})")
                else:
                    self.text.append(f"sw {value}, ({variable.arrayAddress})")
        return value

    def visitArray(self, node: ArrayNode):
        array = self.cur_symbol_table.get_symbol(node.name)["reg"]
        # Has to be int (t register)
        index = self.getValue(node.index.generateMips(self))
        result = None
        address = Register()
        address.assign(7, "t")
        tempRegister = Register()
        tempRegister.assign(self.treg + 1, "t")
        # index * self.size
        self.text.append(tempRegister.save(array.size))
        self.text.append(multiply(address, index, tempRegister))
        self.text.append(neg(address, address))

        if isinstance(array, GlobalArray):
            if array.type == "float":
                result = array.loadGlobal(self.freg, address)
                self.freg += 1
            else:
                result = array.loadGlobal(index.register, address)
            # address = arrayAddress(tempRegister) - indexOffset(address)
            self.text.append(array.loadAddress(tempRegister.register))
            self.text.append(sub(address, tempRegister, address))

        # (self.offset - sp) + index
        elif isinstance(array, LocalArray):
            self.text.append(tempRegister.save(array.offset))
            # address = arrayLocation(array.offset) - indexOffset(address)
            self.text.append(add(address, tempRegister, address))
            if array.type == "float":
                result = array.loadLocal(self.freg, address)
                self.freg += 1
            else:
                result = array.loadLocal(index.register, address)

        ab = result[1]
        ab.arrayAddress = address
        ab.arraySize = array.arraySize
        self.text.append(result[0])
        return ab

    def visitReturn(self, node: ReturnNode):
        if self.main and node.returnValue:
            if node.returnValue.type == "literal":
                if node.returnValue.value == str(0):
                    self.text.append("\n# End MIPS Program")
                    self.text.append("li $v0, 10")
                    self.text.append("syscall")
                    return

        if node.returnValue != "void":
            toReturn = self.getValue(node.returnValue.generateMips(self))
            # steken in $v0
            if toReturn.type == "f":
                self.text.append(f"mfc1 $v0, {toReturn}")
            else:
                self.text.append(f"move $v0, {toReturn}")
        if self.main and node.returnValue:
            self.text.append("\n# End MIPS Program")
            self.text.append("move $a0, $v0")
            self.text.append("li $v0, 17")
            self.text.append("syscall")
        elif self.main:
            self.text.append("\n# End MIPS Program")
            self.text.append("li $v0, 10")
            self.text.append("syscall")
        else:
            # Not Main Function
            #assert(len(self.fs)==2)
            # self.restoreRegisters("","")

            # self.restoreRegisters(self.fs[0], self.fs[1])
            self.text.append("jr $ra")


    def visitBreak(self, node: BreakNode):
        # Mag enkel in While
        # In while loop -> springen naar While Done
        label: str = "WHILE_DONE_" + str(self.while_label)
        self.text.append("b " + label)


    def visitContinue(self, node: ContinueNode):
        # Mag enkel in While
        # In while loop -> Deze iteratie overslaan -> Springen naar While begin
        label: str = "WHILE_" + str(self.while_label)
        self.text.append("b " + label)

    def save(self):
        #print(caller, "begin", self.sp, flush=True)
        self.text.append(f"sw $ra, 0($sp)")
        self.text.append(f"addi $sp, $sp, -4")

        for i in range(0, 7):
            self.text.append(f"sw $t{i}, 0($sp)")
            self.text.append(f"addi $sp, $sp, -4")

        for i in range(0, 7):
            self.text.append(f"s.s $f{i}, 0($sp)")
            self.text.append(f"addi $sp, $sp, -4")

        # Save Stack Pointer in Stack
        self.text.append(f"sw $fp, 0($sp)")
        self.text.append(f"addi $sp, $sp, -4")

        self.text.append(f"addi $fp ,$sp, 0")

    def restoreRegisters(self):
        self.text.append(f"addi $sp ,$fp, 0")

        # Set Stack Pointer ,from Stack
        self.text.append(f"addi $sp, $sp, 4")
        self.text.append(f"lw $fp, 0($sp)")

        for i in range(7, -1, -1):
            self.text.append(f"addi $sp, $sp, 4")
            self.text.append(f"l.s $f{i}, 0($sp)")

        for i in range(7, -1, -1):
            self.text.append(f"addi $sp, $sp, 4")
            self.text.append(f"lw $t{i}, 0($sp)")

        self.text.append(f"addi $sp, $sp, 4")
        self.text.append(f"lw $ra, 0($sp)")

    def visitFunction(self, node: FunctionNode):
        assert isinstance(node, FunctionNode)

        self.functions.append(node.declaration)
        if node.block is None or isinstance(node.block, list):
            return
        self.offset = 0
        declaration = node.declaration
        label: str = declaration.name
        if label == "main":
            self.main = True
            self.text.append(".globl main")

        self.text.append(label + ": ")
        if label != "main":
            self.save()
        else:
            self.treg = 0
            self.freg = 0

        # Functie argumenten parsen
        # De argumenten zullen steken in $4-7/$a0-3
        # We steken deze in de $sp met offset met 'sw'
        amt = len(declaration.arguments)
        if amt > 4:
            raise Exception("Too many arguments.")

        # Arguments initializen
        for i in range(amt):
            func_arg: FunctionArgNode = declaration.arguments[i]
            type1 = func_arg.varType
            print(func_arg.name, end=" ")
            newLocal = self.declareLocal(type1)
            self.cur_symbol_table.add_symbol(func_arg.name, type1, True, newLocal)

            a: str = "$a" + str(i)
            self.text.append(f"sw {a}, 4($sp)")

        # Het blok van de functie
        # In dit blok wordt de return ook verwerkt
        nodeblock: BlockNode = node.block
        assert(isinstance(nodeblock, BlockNode))
        nodeblock.generateMips(self)

        if not self.main:
            self.restoreRegisters()
            self.text.append("jr $ra")
        else:
            self.main = False

    def richerConversion(self, lRegister, rRegister):
        newRegister = Register()
        if (lRegister.type == "float" or rRegister.type == "float") and lRegister.type != rRegister.type:
            if rRegister.type != "f":
                newRegister.assign(self.freg, "f")
                self.freg += 1
                if rRegister.type == "t":
                    self.treg -= 1
                self.text.append(convert_int_to_float(newRegister, rRegister))
                rRegister = newRegister
            elif lRegister.type != "f":
                newRegister.assign(self.freg, "f")
                self.freg += 1
                if lRegister.type == "t":
                    self.treg -= 1
                self.text.append(convert_int_to_float(newRegister, lRegister))
                lRegister = newRegister
        return lRegister, rRegister

    def poorerConversion(self, lRegister, rRegister):
        newRegister = Register()
        if (lRegister.type == "float" or rRegister.type == "float") and lRegister.type != rRegister.type:
            if rRegister.type == "f":
                newRegister.assign(self.treg, "t")
                self.treg += 1
                self.freg -= 1
                self.text.append(convert_float_to_int(newRegister, rRegister))
                rRegister = newRegister
            elif lRegister.type == "f":
                newRegister.assign(self.treg, "t")
                self.treg += 1
                self.freg -= 1
                self.text.append(convert_float_to_int(newRegister, lRegister))
                lRegister = newRegister
        return lRegister, rRegister

    def visitBlock(self, node: BlockNode):
        new_name = self.cur_symbol_table.name.copy()
        new_id = 0 + len(self.cur_symbol_table.subScopes)
        new_name.append(new_id)
        new_st = SymbolTable(new_name)
        new_st.parentScope = self.cur_symbol_table
        self.cur_symbol_table.subScopes.append(new_st)
        self.cur_symbol_table = new_st

        for statement in node.children:
            statement.generateMips(self)

        self.cur_symbol_table = self.cur_symbol_table.parentScope

    def visitExpressionStatement(self, node: ExpressionStatementNode):
        for statement in node.children:
            self.treg = 0
            self.freg = 0
            statement.generateMips(self)

    def visitPrintf(self, node: PrintfNode):
        int_1 = "d"
        float = "f"
        char = "c"
        string = "s"

        # Parse string with arguments
        s = parse_string(node.string, node.arguments)
        for i in s:
            if isinstance(i, str):
                label: str = self.increase_printf_label()
                # Put string into data
                self.data.append(f"{label}: .asciiz {i}")
                # Put string into $a0
                self.text.append(f"la $a0, {label}")
                # Call Printf Function
                self.text.append("jal printf_string\n")
            else:
                # i[1]: Literal/ TermNode/ Variabele / ...
                if i[1].type == "variable":
                    result = self.getValue(self.cur_symbol_table.get_symbol(i[1].name)["reg"])
                else:
                    gm = i[1].generateMips(self)
                    result: Register = self.getValue(gm)
                if i[0] == int_1:

                    # Deze reg nu printen
                    # Register value extracten
                    # Put string into $a0
                    self.text.append(f"move $a0, {result}")

                    self.save()

                    # Call Printf Function
                    self.text.append("jal printf_int")
                    self.restoreRegisters()

                elif i[0] == float:
                    # Waarde steken in $f12
                    self.text.append(f"mov.s $f12, {result}")

                    self.save()

                    # Call Printf Function
                    self.text.append("jal printf_float")
                    self.restoreRegisters()

                elif i[0] == string:

                    # TODO ADD GLOBAL
                    # tfp: list[int] = self.save()
                    # treg = tfp[0]
                    # freg = tfp[1]
                    # TODO

                    tempRegister = Register()
                    tempRegister.assign(self.treg, "t")
                    for k in range(result.arraySize):
                        self.text.append(f"li {tempRegister}, {result.offset - k}")
                        self.text.append(f"lb $a0, ({tempRegister})")
                        self.text.append("jal printf_char\n")
                #
                elif i[0] == char:

                    self.text.append(f"move $a0, {result}")

                    self.save()

                    self.text.append("jal printf_char\n")
                    self.restoreRegisters()

                else:
                    print("error676" + i[0])

    def visitScanf(self, node: ScanfNode):
        self.save()

        int_1 = "d"
        float = "f"
        char = "c"
        string = "s"
        value = None

        # Parse string
        parsed: list[str] = compile_scanf_string(node.string)
        for i in range(0, len(parsed)):
            variable_name: str = node.arguments[i].value.variable.name

            # bv. arg: string/int/float/char = &x

            register = self.cur_symbol_table.get_symbol(variable_name)['reg']
            r: str = str(register.register)

            dest = None
            if register.type == "s":
                dest = "$s" + r
            elif register.type == "t":
                dest = "t" + r
            else:
                dest = "t" + r

            if parsed[i][0:1] == string:
                label = self.increase_scanf_label()

                size_str = parsed[i][1:]
                size = int(size_str)
                self.data.append(f"{label}: .space {size+1}")
                self.text.append("la $a0, " + label)
                self.text.append(f"li $a1, {size+1}")

                # Call Scanf Function
                self.text.append("jal scanf_string")
                # Input in {label}

                tempRegister = Register()
                tempRegister2 = Register()
                tempRegister.assign(self.treg, "t")
                tempRegister2.assign(self.treg+1, "t")
                for k in range(size):
                    self.text.append(f"\nla {tempRegister}, {label}")
                    self.text.append(f"addi {tempRegister}, {tempRegister}, {k}")
                    self.text.append(f"lb {tempRegister}, ({tempRegister})")
                    self.text.append(f"li {tempRegister2}, {register.offset - k}")
                    self.text.append(f"sb {tempRegister}, ({tempRegister2})")
            elif parsed[i] == char:
                self.text.append("jal scanf_char")
                # User input in v0
                #print("dit is scanf", register.offset, self.sp, flush=True)
                self.text.append(f"sw $v0, {register.offset}($sp)")



            elif parsed[i] == int_1:
                self.text.append("jal scanf_int")
                # User Input in $v0

                #print("dit is scanf", register.offset, self.sp, flush=True)
                self.text.append(f"sw $v0, {register.offset}($sp)")
                # self.text.append(f"la ${dest} , ($v0)\n")

            # restore temp regsiters
            self.text.append("li $a0, '\\n'")
            self.text.append("jal printf_char")

            self.restoreRegisters()

            # self.text.append(f"addi $sp, $sp, 4")
            # self.sp += 4

    def find_function(self, name):
        for i in self.functions:
            if i.name == name:
                return i
        return None

    def visitFunction_call(self, node: CallNode):
        # Arguments in registers a0-3 plaatsen
        a_ctr: int = 0
        for i in node.arguments:
            if isinstance(i, str):
                label: str = self.increase_printf_label()
                self.data.append(f"{label}: .asciiz {i}")
                self.text.append(f"move $a{str(a_ctr)}, {label}")
            else:
                # Argument is Term/variable/ ....
                arg = self.getValue(i.value.generateMips(self))
                self.text.append(f"move $a{str(a_ctr)}, {arg}")
                if arg.type == "f":
                    self.freg -= 1
                elif arg.type == "t":
                    self.treg -= 1
                else:
                    print("error900")
            a_ctr += 1


        # Functie oproepen
        self.text.append("jal " + node.name + " \n")

        # Get Function Return 'Type'
        found_func = self.find_function(node.name)
        rt: str = ""
        if found_func is None:
            print("error886")
        else:
            rt = self.find_function(node.name).returnType

        # Return waarde uit v0 halen en steken in t-register
        returnRegister = Register()

        if rt == "float":
            returnRegister.assign(self.freg, "f")
            self.freg += 1
            self.text.append(f"mtc1 {returnRegister}, $v0")
        else:
            returnRegister.assign(self.treg, "t")
            self.treg += 1
            self.text.append(f"move {returnRegister}, $v0")

        return returnRegister

    def includeStdio(self):
        # Printf functie implementeren
        # Value to be printed needs to be in $a0
        self.text.append("printf_string: # Print A String")
        self.text.append("li $v0, 4") # Print String
        self.text.append("syscall")
        self.text.append("jr $ra")

        self.text.append("")

        self.text.append("printf_char: # Print A Char")
        self.text.append("li $v0, 11")  # Print Char
        self.text.append("syscall")
        self.text.append("jr $ra")

        self.text.append("")

        self.text.append("printf_int: # Print An Integer")
        self.text.append("li $v0, 1")  # Print String
        self.text.append("syscall")
        self.text.append("jr $ra")

        self.text.append("")

        self.text.append("printf_float: # Print A Float")
        self.text.append("li $v0, 2")  # Print String
        self.text.append("syscall")
        self.text.append("jr $ra")

        self.text.append("")

        # Scanf functie implementeren
        self.text.append("scanf_string:")
        self.text.append("li $v0, 8")
        self.text.append("syscall")
        self.text.append("jr $ra")
        # User Input will be in {label}

        self.text.append("")

        self.text.append("scanf_char:")
        self.text.append("li $v0, 12")
        self.text.append("syscall")
        self.text.append("jr $ra")
        # User Input will be in $v0
        self.text.append("")

        self.text.append("scanf_int:")
        self.text.append("li $v0, 5")
        self.text.append("syscall")
        self.text.append("jr $ra")
        # User Input will be in $v0
        self.text.append("")


    def visitComment(self, node: CommentNode):
        self.text.append("# " + node.text)


