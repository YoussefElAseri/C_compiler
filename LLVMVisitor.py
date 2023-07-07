from Nodes import *
from LLVMOperations import *


class LLVMVisitor:
    def __init__(self):
        self.instructions = list()
        self.varNames = 1
        self.file = ""
        self.symbolTable = dict()
        # block labels
        self.blocks = []

    # return a name for a temporary variable
    def tempVar(self):
        name = f"%{self.varNames}"
        self.varNames += 1
        return name

    def visitRun(self, node: RunNode):
        self.instructions.append('declare i32 @printf(i8*, ...)\n'
                                 '@intFormat = private constant [4 x i8] c"%d\\0A\\00"'
                                 '@floatFormat = private constant [4 x i8] c"%f\\0A\\00"')
        self.instructions.append('define void @printInt(i32 %a) '
                                 '{\n'
                                 '%p = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8],\n'
                                 '[4 x i8]* @intFormat,i32 0, i32 0), i32 %a)\n'
                                 'ret void\n'
                                 '}\n')
        self.instructions.append('define void @printFloat(float %a) '
                                 '{\n'
                                 '%p = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8],\n'
                                 '[4 x i8]* @floatFormat,i32 0, i32 0), float %a)\n'
                                 'ret void\n'
                                 '}\n')
        self.instructions.append('define i1 @"main"()')
        self.instructions.append('{')
        for child in node.children:
            child.generateCode(self)
        self.instructions.append("ret i1 0")
        self.instructions.append('}')
        file = open(self.file, "w")
        for instruction in self.instructions:
            file.write(instruction + '\n')
        file.close()

    def visitPrint(self, node: PrintNode):
        printInput = self.getValue(self.symbolTable["%" + node.toPrint])
        if printInput.varType == "float":

            # TODO: always prints zero

            self.instructions.append(f"call void @printFloat({printInput.varType} {printInput})")
        elif printInput.varType == "i32":
            self.instructions.append(f"call void @printInt({printInput.varType} {printInput})")
        else:
            raise Exception(f"invalid print type")

    def visitLine(self, node: StatementNode):
        if node.comment:
            node.comment.generateCode(self)
        if node.statement:
            node.statement.generateCode(self)

    def visitIf(self, node: IfNode):
        # condition check
        result = node.condition.generateCode(self)
        # make new label
        br1 = self.tempVar()[1:]
        self.blocks.append(br1)
        index = len(self.instructions)
        self.instructions.append(f"\n{br1}:")
        node.block.generateCode(self)
        if node.elseNode is not None:
            index2 = len(self.instructions)
            node.elseNode.generateCode(self)
        br2 = self.tempVar()[1:]
        self.blocks.append(br2)
        self.instructions.insert(index, f"br i1 {result.name}, label %{br1}, label %{br2}")
        self.instructions.append(f"br label %{br2}")
        if node.elseNode is not None:
            self.instructions.insert(index2+1, f"br label %{br2}")
        self.instructions.append(f"\n{br2}:")

    def visitElse(self, node: ElseNode):
        br = self.tempVar()[1:]
        self.blocks.append(br)
        self.instructions.append(f"\n{br}:")
        node.block.generateCode(self)

    def visitWhile(self, node: WhileNode):
        br1 = self.tempVar()[1:]
        self.blocks.append(br1)
        self.instructions.append(f"br label %{br1}")
        self.instructions.append(f"\n{br1}:")
        result = node.condition.generateCode(self)
        # for the first segment
        index1 = len(self.instructions)
        br2 = self.tempVar()[1:]
        self.blocks.append(br2)
        self.instructions.append(f"\n{br2}:")
        # breakIndex = node.block.generateCode(self)
        self.instructions.append(f"br label %{br1}")
        br3 = self.tempVar()[1:]
        self.blocks.append(br3)
        self.instructions.append(f"\n{br3}:")
        self.instructions.insert(index1, f"br i1 {result}, label %{br2}, label %{br3}")
        # if breakIndex is not None:
        #     self.instructions.insert(breakIndex, f"br label %{br3}")

    def visitBreak(self, node: BreakNode):
        return len(self.instructions)

    def visitContinue(self, node: ContinueNode):
        self.instructions.append(f"br label %{self.blocks[-1]}")

    def visitExpressionStatement(self, node: ExpressionStatementNode):
        self.instructions.append("; " + node.instruction)
        for child in node.children:
            child.generateCode(self)

    def visitComment(self, node: CommentNode):
        newText = node.text.split('\n')
        for line in newText:
            self.instructions.append("; " + line)

    def visitAssignment(self, node: AssignmentNode):
        variable = node.left.generateCode(self)
        # eerst checken of het een pointer is
        if node.right.type == "literal" and "float" in variable.varType:
            if node.right.literalType == "int":
                node.right.literalType = "float"
        result = node.right.generateCode(self)
        if result.address:
            self.instructions.append(store(result, variable))
            return
        tempResult = result
        result = self.getValue(result)

        # als result al één of meerdere keren gedereferenced werd, dan zal het niet opnieuw gebeuren
        # in getValue() wat wel moet
        if tempResult == result and result.varType[-1] == "*":
            temp = load(self.tempVar(), result)
            result = temp[0]
            self.instructions.append(temp[1])
        # implicit conversions

        # if variable.varType != "float" and result.varType == "float":
        #     toInt = fptosi(self.tempVar(), result)
        #     result = toInt[0]
        #     self.instructions.append(toInt[1])
        # elif variable.varType == "float" and result.varType != "float":
        #     toFloat = sitofp(self.tempVar(), result)
        #     result = toFloat[0]
        #     self.instructions.append(toFloat[1])
        # if variable.varType != result.varType:
        #     tempConversion = None
        #     if result.varType == "i32":
        #         tempConversion = trunc(self.tempVar(), result, variable.varType)
        #     elif variable.varType == "i32":
        #         tempConversion = zext(self.tempVar(), result, variable.varType)
        #     elif result.varType == "i8":
        #         tempConversion = trunc(self.tempVar(), result, variable.varType)
        #     elif variable.varType == "i8":
        #         tempConversion = zext(self.tempVar(), result, variable.varType)
        #     result = tempConversion[0]
        #     self.instructions.append(tempConversion[1])

        self.instructions.append(store(result, variable))

    def visitInstantiation(self, node: InstantiationNode):
        temp = alloca("%" + node.name, node.varType)
        variable = temp[0]
        self.instructions.append(temp[1])
        self.symbolTable["%"+node.name] = variable
        return variable

    def visitVariable(self, node: VariableNode):
        return self.symbolTable["%" + node.name]

    def visitLiteral(self, node: LiteralNode):
        return convertNode(node)

    def visitLogic(self, node: LogicNode):
        leftVal = self.getValue(node.left.generateCode(self))
        rightVal = self.getValue(node.right.generateCode(self))
        temp = self.richerConversion(leftVal, rightVal)
        leftVal = temp[0]
        rightVal = temp[1]
        floatType = temp[2]
        if floatType:
            if node.operation == "&&":
                temp = fcmpLogic("and", self.tempVar(), self.tempVar(), self.tempVar(), leftVal, rightVal)
            elif node.operation == "||":
                temp = fcmpLogic("or", self.tempVar(), self.tempVar(), self.tempVar(), leftVal, rightVal)
        else:
            if node.operation == "&&":
                temp = logic("and", self.tempVar(), leftVal, rightVal)
            elif node.operation == "||":
                temp = logic("or", self.tempVar(), leftVal, rightVal)
        result = temp[0]
        self.instructions.append(temp[1])
        return result

    def visitCompare(self, node: CompareNode):
        leftVal = self.getValue(node.left.generateCode(self))
        rightVal = self.getValue(node.right.generateCode(self))
        keyword = ""
        temp = self.richerConversion(leftVal, rightVal)
        leftVal = temp[0]
        rightVal = temp[1]
        floatType = temp[2]
        if floatType:
            if node.operation == "<":
                keyword = "olt"
            elif node.operation == "<=":
                keyword = "ole"
            elif node.operation == "==":
                keyword = "oeq"
            elif node.operation == "!=":
                keyword = "one"
            elif node.operation == ">=":
                keyword = "oge"
            elif node.operation == ">":
                keyword = "ogt"
            temp = fcmp(keyword, self.tempVar(), leftVal, rightVal)
            result = temp[0]
            self.instructions.append(temp[1])
        else:
            if node.operation == "<":
                keyword = "slt"
            elif node.operation == "<=":
                keyword = "sle"
            elif node.operation == "==":
                keyword = "eq"
            elif node.operation == "!=":
                keyword = "ne"
            elif node.operation == ">=":
                keyword = "sge"
            elif node.operation == ">":
                keyword = "sgt"
            temp = icmp(keyword, self.tempVar(), leftVal, rightVal)
            result = temp[0]
            self.instructions.append(temp[1])
        return result

    def visitTerm(self, node: TermNode):
        leftVal = self.getValue(node.left.generateCode(self))
        rightVal = self.getValue(node.right.generateCode(self))
        temp = self.richerConversion(leftVal, rightVal)
        leftVal = temp[0]
        rightVal = temp[1]
        floatType = temp[2]
        if floatType:
            if node.operation == "+":
                temp = fadd(self.tempVar(), leftVal, rightVal)
            elif node.operation == "-":
                temp = fsub(self.tempVar(), leftVal, rightVal)
        else:
            if node.operation == "+":
                temp = add(self.tempVar(), leftVal, rightVal)
            elif node.operation == "-":
                temp = sub(self.tempVar(), leftVal, rightVal)
        result = temp[0]
        self.instructions.append(temp[1])
        return result

    def visitFactor(self, node: FactorNode):
        leftVal = self.getValue(node.left.generateCode(self))
        rightVal = self.getValue(node.right.generateCode(self))
        temp = self.richerConversion(leftVal, rightVal)
        leftVal = temp[0]
        rightVal = temp[1]
        floatType = temp[2]
        if floatType:
            if node.operation == "*":
                temp = fmul(self.tempVar(), leftVal, rightVal)
            elif node.operation == "/":
                temp = fdiv(self.tempVar(), leftVal, rightVal)
            elif node.operation == "%":
                toInt = fptosi(self.tempVar(), leftVal)
                leftVal = toInt[0]
                self.instructions.append(toInt[1])
                toInt = fptosi(self.tempVar(), rightVal)
                rightVal = toInt[0]
                self.instructions.append(toInt[1])
                temp = urem(self.tempVar(), leftVal, rightVal)
        else:
            if node.operation == "*":
                temp = mul(self.tempVar(), leftVal, rightVal)
            elif node.operation == "/":
                temp = div(self.tempVar(), leftVal, rightVal)
            elif node.operation == "%":
                temp = urem(self.tempVar(), leftVal, rightVal)
        result = temp[0]
        self.instructions.append(temp[1])
        return result

    def visitUnary(self, node: UnaryNode):
        val = node.variable.generateCode(self)
        if node.operation == "&":
            val.address = True
            return val
        elif node.operation == "*":
            temp = load(self.tempVar(), val)
            result = temp[0]
            self.instructions.append(temp[1])
            return result
        val = self.getValue(val)
        temp = None
        floatType = False
        if val.varType == "float":
            floatType = True
        if node.operation == "-":
            if floatType:
                temp = fneg(self.tempVar(), val)
            else:
                temp = neg(self.tempVar(), val)
        elif node.operation == "!":
            if floatType:
                toInt = fptosi(self.tempVar(), val)
                val = toInt[0]
                self.instructions.append(toInt[1])
            temp = xor(self.tempVar(), val, LlvmType("i32", 1))
        result = temp[0]
        self.instructions.append(temp[1])
        return result

    def visitTypeCast(self, node: TypeCastNode):
        value = self.getValue(node.variable.generateCode(self))
        cast = node.castTo
        newValue = None
        if cast == "float" and value.varType != "float":
            conversion = sitofp(self.tempVar(), value)
            value = conversion[0]
            self.instructions.append(conversion[1])
        elif cast != "float" and value.varType == "float":
            conversion = fptosi(self.tempVar(), value)
            value = conversion[0]
            self.instructions.append(conversion[1])
        if ((cast == "float" and value.varType == "float") or
                (cast == "int" and value.varType == "i32") or
                (cast == "char" and value.varType == "i8") or
                (cast == "bool" and value.varType == "i1")):
            newValue = value
        elif cast != value.varType:
            conversion = None
            if cast == "int":
                conversion = zext(self.tempVar(), value, "i32")
            elif cast == "char":
                if value.varType == "i32":
                    conversion = trunc(self.tempVar(), value, "i8")
                elif value.varType == "i1":
                    conversion = zext(self.tempVar(), value, "i8")
            elif cast == "bool":
                conversion = trunc(self.tempVar(), value, "i1")
            newValue = conversion[0]
            self.instructions.append(conversion[1])

        return newValue

    def visitSpecialUnary(self, node: SpecialUnaryNode):
        val = self.getValue(node.variable.generateCode(self))
        temp = None
        floatType = False
        if val.varType == "float":
            floatType = True
        if node.operation == "++":
            if floatType:
                temp = fadd(self.tempVar(), val, LlvmType("float", 1))
            else:
                temp = add(self.tempVar(), val, LlvmType("i32", 1))
        elif node.operation == "--":
            if floatType:
                temp = fsub(self.tempVar(), val, LlvmType("float", 1))
            else:
                temp = sub(self.tempVar(), val, LlvmType("i32", 1))
        result = temp[0]
        self.instructions.append(temp[1])
        return result

    def richerConversion(self, leftVal, rightVal):
        floatType = False
        temp = None
        if leftVal.varType == "float" or rightVal.varType == "float":
            floatType = True
        if (leftVal.varType == "float" or rightVal.varType == "float") and leftVal.varType != rightVal.varType:
            if rightVal.varType != "float":
                temp = sitofp(self.tempVar(), rightVal)
                rightVal = temp[0]
            elif leftVal.varType != "float":
                temp = sitofp(self.tempVar(), leftVal)
                leftVal = temp[0]
            self.instructions.append(temp[1])
        elif leftVal.varType != rightVal.varType:
            if leftVal.varType == "i32":
                temp = zext(self.tempVar(), rightVal, "i32")
                rightVal = temp[0]
            elif rightVal == "i32":
                temp = zext(self.tempVar(), rightVal, "i32")
                leftVal = temp[0]
            elif leftVal.varType == "i8":
                temp = zext(self.tempVar(), rightVal, "i8")
                rightVal = temp[0]
            elif rightVal == "i8":
                temp = zext(self.tempVar(), rightVal, "i8")
                leftVal = temp[0]
            self.instructions.append(temp[1])
        return leftVal, rightVal, floatType

    def getValue(self, variable):
        if variable.name in self.symbolTable:
            temp = load(self.tempVar(), variable)
            currentVariable = temp[0]
            self.instructions.append(temp[1])
        else:
            currentVariable = variable
        return currentVariable


def float_to_64bit_hex(x):
    if isinstance(x, str):
        x = float(x)
    bytes_of_x = struct.pack('>f', x)
    x_as_int = struct.unpack('>f', bytes_of_x)[0]
    x_as_double = struct.pack('>d', x_as_int).hex()
    x_as_double = '0x' + x_as_double
    return x_as_double


def convertNode(node: LiteralNode):
    value = node.convertValType()
    nlt = str(node.literalType)
    if nlt == "int":
        return LlvmType("i32", value)
    elif nlt == "float":
        return LlvmType("float", float_to_64bit_hex(value))
    elif nlt == "char":
        return LlvmType("i8", ord(value))
    elif nlt == "bool":
        if value:
            return LlvmType("i1", 1)
        return LlvmType("i1", 0)
    raise Exception(f"Node Literal Type '{nlt}' not supported")
