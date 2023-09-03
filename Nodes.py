# Checks if operation is valid and returns the highest order
# Only use for factor, term, logic and comparison
def getHighestOrder(left, right):
    for i in [left, right]:
        if "*" in i or "[]" in i or i == "address":
            raise Exception(f"Incompatible types {left} and {right}!")

    if left == "float" or right == "float":
        return "float"
    elif left == "int" or right == "int":
        return "int"
    elif left == "char" or right == "char":
        return "char"
    elif left == "bool" or right == "bool":
        return "bool"
    else:
        raise Exception(f"Unknown type {left} or {right} in getHighestOrder!")


class Node:
    children = []
    type = "base"

    def __init__(self):
        self.children = []

    def addNodes(self, nodes):
        self.children.append(nodes)

    def constantFolding(self):
        for child in self.children:
            newNode = child.constantFolding()
            if newNode:
                self.children[self.children.index(child)] = newNode
        return False

    def checkOperationsValidity(self, table):
        for child in self.children:
            child.checkOperationsValidity(table)

    def unusedCleanup(self, table):
        for child in self.children:
            child.unusedCleanup(table)

    def generateLlvm(self, llvm):
        pass

    def generateMips(self, mips, global_var=False):
        pass

    def __repr__(self):
        return "base class"


class RunNode(Node):
    type = "run"
    include = False

    def generateLlvm(self, llvm):
        return llvm.visitRun(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitRun(self)

    def checkOperationsValidity(self, table):
        for child in self.children:
            child.checkOperationsValidity(table)
        table.childIndex = 0

    def unusedCleanup(self, table):
        toDelete = []
        for child in self.children:
            if child.unusedCleanup(table):
                toDelete.append(child)
        self.children = [i for i in self.children if i not in toDelete]
        table.childIndex = 0

    def __repr__(self):
        return "run"


class IncludeNode(Node):
    type = "include"
    lib = "stdio"

    def __repr__(self):
        return self.lib


class FuncDeclareNode(Node):
    type = "function_declaration"
    name = ""
    returnType = ""
    arguments = []

    def __repr__(self):
        return f"{self.returnType} {self.name}"


class FunctionNode(Node):
    type = "function"
    name = ""
    declaration = None  # FuncDeclareNode
    block = None  # BlockNode

    def generateMips(self, mips, global_var=False):
        a = mips.visitFunction(self)
        return a

    def unusedCleanup(self, table):
        self.block.unusedCleanup(table)
        if table.retrieveEntry(self.name)[0]["calls"] == 0 and self.name != "main":
            return True

    def __repr__(self):
        return f"function {self.declaration.name}"


class PrintfNode(Node):
    type = "printf"
    string = None  # bv %d;
    arguments = []  # : list[ArgumentNode]

    def generateMips(self, mips, global_var=False):
        return mips.visitPrintf(self)

    def __repr__(self):
        return f"void printf({self.string})"


class ScanfNode(Node):
    type = "scanf"
    string = None
    arguments = []

    def generateMips(self, mips, global_var=False):
        return mips.visitScanf(self)

    def __repr__(self):
        return "void scanf"


class FunctionArgNode(Node):
    type = "function_argument"
    const = None
    varType = None
    name = None

    def __repr__(self):
        if self.const:
            return f"const {self.varType} {self.name}"
        return f"arg: {self.varType} {self.name}"


class CallNode(Node):
    type = "call"
    name = ""
    arguments = []

    def generateMips(self, mips, global_var=False):
        return mips.visitFunction_call(self)

    def __repr__(self):
        return f"call: {self.name}"


class ArgumentNode(Node):
    type = "argument"
    value = None

    def __repr__(self):
        return f"arg: {self.value}"


class BreakNode(Node):
    type = "break"
    context = ""

    def generateLlvm(self, llvm):
        return llvm.visitBreak(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitBreak(self)

    def __repr__(self):
        return "break"


class ContinueNode(Node):
    type = "continue"
    context = ""

    def generateLlvm(self, llvm):
        return llvm.visitContinue(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitContinue(self)

    def __repr__(self):
        return "continue"


class ReturnNode(Node):
    type = "return"
    context = ""
    returnType = ""
    returnValue = None

    def checkOperationsValidity(self, table):
        rType = self.returnValue.checkOperationsValidity(table)
        highestType = getHighestOrder(self.returnType, rType)
        if highestType == rType and self.returnType != rType:
            print(f"Warning: implicitly converting {rType} to {self.returnType}", flush=True)

    def constantFolding(self):
        newNode = self.returnValue.constantFolding()
        if newNode:
            self.returnValue = newNode
            self.children[0] = newNode
        return False

    def convert(self, node):
        if node.type == "variable":
            return node.name
        elif node.type == "literal":
            return node.value
        else:
            print("error120")

    def getargs(self, args):
        call_args = []
        for ca in args:
            if ca.value.type == "unary":
                type = ca.value.variable.name
                call_args.append(type + "*")
            elif ca.value.type == "variable":
                call_args.append(ca.value.name)
            elif ca.value.type == "term":
                call_args.append("")
            else:
                call_args.append(ca.value.literalType)
        return call_args

    def generateMips(self, mips, global_var=False):
        return mips.visitReturn(self)

    def __repr__(self):
        return f"return"


class BlockNode(Node):
    type = "block"
    # all code inside
    block = []
    comment = ""

    def checkOperationsValidity(self, table):
        newTable = table.childScopes[table.childIndex]
        table.childIndex += 1
        for child in self.children:
            child.checkOperationsValidity(newTable)
        newTable.childIndex = 0

    def constantFolding(self):
        for child in self.children:
            newNode = child.constantFolding()
            if newNode:
                self.children[self.children.index(child)] = newNode
        self.block = self.children
        return self

    def unusedCleanup(self, table):
        toDelete = []
        newTable = table.childScopes[table.childIndex]
        table.childIndex += 1
        for child in self.children:
            if child.unusedCleanup(newTable):
                toDelete.append(child)
        self.children = [i for i in self.children if i not in toDelete]
        self.block = self.children
        newTable.childIndex = 0

    def generateLlvm(self, llvm):
        for i in self.children:
            i.generateLlvm(llvm)

    def generateMips(self, mips, global_var=False):
        mips.visitBlock(self)

    def __repr__(self):
        return f"start scope"


class StatementNode(Node):
    # Een statementNode heeft altijd maximum 1 kind
    type = "line"
    statement = None
    comment = None

    def generateLlvm(self, llvm):
        return llvm.visitLine(self)

    def generateMips(self, mips, global_var=False):
        if self.comment:
            self.comment.generateMips(mips)
        # if self.statement:
        #     mips.text.append("")
        #     instr = self.instruction
        #     instr = instr.split("\n")
        #     for i in instr:
        #         mips.text.append("# " + i)
        self.statement.generateMips(mips)

    def unusedCleanup(self, table):
        return self.statement.unusedCleanup(table)

    def __repr__(self):
        return "line"


class IfNode(Node):
    type = "if"
    condition = None
    # all code inside
    block = None
    elseNode = None
    comment = None

    @staticmethod
    def checkTrueOrFalse(literal):
        if literal.convertValType():
            return True
        return False

    # Also checks if the condition is always true
    def constantFolding(self):
        for child in self.children:
            newNode = child.constantFolding()
            if newNode:
                self.children[self.children.index(child)] = newNode
        if not isinstance(self.condition, LiteralNode):
            return False

        condition = self.checkTrueOrFalse(self.condition)

        # If condition is always true delete else and 'change' if into BlockNode
        # If condition is always false delete if and 'change' else into BlockNode
        # If condition is always false and else exists, 'change' if into BlockNode
        if condition:
            if self.elseNode:
                self.children.remove(self.elseNode)
                self.elseNode = None
            return self.block
        else:
            if self.elseNode:
                self.block = self.elseNode.block
                return self.block
            else:
                return BlockNode()

    def generateLlvm(self, llvm):
        return llvm.visitIf(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitIf(self)

    def __repr__(self):
        return "if"


class ElseNode(Node):
    type = "else"
    # all code inside
    block = None

    def generateLlvm(self, llvm):
        return llvm.visitElse(self)

    def generateMips(self, mips, global_var=False):
        mips.visitBlock(self.block)

    def __repr__(self):
        return "else"


class WhileNode(Node):
    type = "while"
    condition = None
    block = None
    comment = None

    def generateLlvm(self, llvm):
        return llvm.visitWhile(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitWhile(self)

    def __repr__(self):
        return "while"


class ExpressionStatementNode(Node):
    type = "ExpressionStatement"
    instruction = ""
    # statement is only used to delete in
    statement = None

    def generateLlvm(self, llvm):
        return llvm.visitExpressionStatement(self)

    def generateMips(self, mips, global_var=False):
        mips.text.append(f"\n ## {self.instruction}")
        return mips.visitExpressionStatement(self)

    def unusedCleanup(self, table):
        toDelete = []
        for child in self.children:
            delete = child.unusedCleanup(table)
            if delete and isinstance(child, AssignmentNode):
                self.children[self.children.index(child)] = child.right
            elif delete and isinstance(child, InstantiationNode):
                toDelete.append(child)
        self.children = [i for i in self.children if i not in toDelete]

        if not self.children:
            return True
        return False

    def __repr__(self):
        return f"instruction: {self.instruction}"


class CommentNode(Node):
    type = "comment"
    text = ""

    def generateLlvm(self, llvm):
        return llvm.visitComment(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitComment(self)

    def __repr__(self):
        return f"comment: {self.text}"


class AssignmentNode(Node):
    type = "assignment"
    left = None
    right = None

    def unusedCleanup(self, table):
        return self.left.unusedCleanup(table)

    def checkOperationsValidity(self, table):
        lType = self.left.checkOperationsValidity(table)
        rType = self.right.checkOperationsValidity(table)
        highestType = getHighestOrder(lType, rType)
        if highestType == rType and lType != rType:
            print(f"Warning: implicitly converting {rType} to {lType}", flush=True)

    def constantFolding(self):
        newNode = self.right.constantFolding()
        if newNode:
            self.right = newNode
            self.children[1] = newNode
        return False

    def generateLlvm(self, llvm):
        return llvm.visitAssignment(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitAssignment(self, global_var)

    def __repr__(self):
        return "="


class InstantiationNode(Node):
    type = "instantiation"
    const = False
    varType = ""  # type int, float, ...
    name = ""  # variable name x, y , ...

    def unusedCleanup(self, table):
        if table.retrieveEntry(self.name)[0]["uses"] == 0:
            return True

    def checkOperationsValidity(self, table):
        return self.varType

    def generateLlvm(self, llvm):
        return llvm.visitInstantiation(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitInstantiation(self, global_var)

    def __repr__(self):
        if self.const:
            return f"const {self.varType} {self.name}"
        return f"{self.varType} {self.name}"


class VariableNode(Node):
    type = "variable"
    name = ""

    def unusedCleanup(self, table):
        if table.retrieveEntry(self.name)[0]["uses"] == 0:
            return True

    def checkOperationsValidity(self, table):
        return table.retrieveEntry(self.name)[0]["type"]

    def generateLlvm(self, llvm):
        return llvm.visitVariable(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitVariable(self)

    def __repr__(self):
        return self.name


class ArrayInstantiationNode(Node):
    type = "arrayInstantiation"
    name = ""
    size = None
    varType = ""

    def checkOperationsValidity(self, table):
        return f"{self.varType}[]"

    def generateMips(self, mips, global_var=False):
        return mips.visitArrayInstantiation(self, global_var)

    def unusedCleanup(self, table):
        if table.retrieveEntry(self.name)[0]["uses"] == 0:
            return True

    def __repr__(self):
        return f"{self.varType} {self.name}[{self.size}]"


class ArrayNode(Node):
    type = "array"
    name = ""
    index = None
    variableType = ""

    def checkOperationsValidity(self, table):
        return table.retrieveEntry(self.name)[0]["variableType"] + "[]"

    def generateMips(self, mips, global_var=False):
        return mips.visitArray(self)

    def __repr__(self):
        return f"{self.name}[{self.index}]"


class LogicNode(Node):
    type = "logic"
    operation = ""
    left = None
    right = None

    def checkOperationsValidity(self, table):
        lType = self.left.checkOperationsValidity(table)
        rType = self.right.checkOperationsValidity(table)
        # run just for the type checking
        getHighestOrder(lType, rType)
        return "bool"

    def constantFolding(self):
        lVariable = self.left.constantFolding()
        rVariable = self.right.constantFolding()
        if not lVariable and not rVariable:
            return False
        elif lVariable and not rVariable:
            self.children[self.children.index(self.left)] = lVariable
            self.left = lVariable
            return self
        elif not lVariable and rVariable:
            self.children[self.children.index(self.right)] = rVariable
            self.right = rVariable
            return self

        newVariable = LiteralNode()
        newVariable.literalType = "bool"
        lValue = lVariable.convertValType()
        rValue = rVariable.convertValType()
        newValue = False

        if self.operation == "&&":
            newValue = lValue and rValue
        elif self.operation == "||":
            newValue = lValue or rValue

        if newValue:
            newVariable.value = "true"
        else:
            newVariable.value = "false"

        return newVariable

    def generateLlvm(self, llvm):
        return llvm.visitLogic(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitLogic(self)

    def __repr__(self):
        return self.operation


class CompareNode(Node):
    type = "compare"
    operation = ""
    left = None
    right = None

    def checkOperationsValidity(self, table):
        lType = self.left.checkOperationsValidity(table)
        rType = self.right.checkOperationsValidity(table)
        # run just for the type checking
        getHighestOrder(lType, rType)
        return "bool"

    def constantFolding(self):
        lVariable = self.left.constantFolding()
        rVariable = self.right.constantFolding()
        if not lVariable and not rVariable:
            return False
        elif lVariable and not rVariable:
            self.children[self.children.index(self.left)] = lVariable
            self.left = lVariable
            return self
        elif not lVariable and rVariable:
            self.children[self.children.index(self.right)] = rVariable
            self.right = rVariable
            return self

        newVariable = LiteralNode()
        lValue = lVariable.convertValType()
        rValue = rVariable.convertValType()
        newVariable.literalType = "bool"

        if self.operation == "<":
            newVariable.value = str(lValue < rValue)
        elif self.operation == "<=":
            newVariable.value = str(lValue <= rValue)
        elif self.operation == "==":
            newVariable.value = str(lValue == rValue)
        elif self.operation == "!=":
            newVariable.value = str(lValue != rValue)
        elif self.operation == ">=":
            newVariable.value = str(lValue >= rValue)
        elif self.operation == ">":
            newVariable.value = str(lValue > rValue)

        return newVariable

    def generateLlvm(self, llvm):
        return llvm.visitCompare(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitCompare(self)

    def __repr__(self):
        return self.operation


class TermNode(Node):
    type = "term"
    operation = ""
    left = None
    right = None
    variableType = ""

    def checkOperationsValidity(self, table):
        lType = self.left.checkOperationsValidity(table)
        rType = self.right.checkOperationsValidity(table)
        return getHighestOrder(lType, rType)

    def constantFolding(self):
        lVariable = self.left.constantFolding()
        rVariable = self.right.constantFolding()
        if not lVariable and not rVariable:
            return False
        elif lVariable and not rVariable:
            self.children[self.children.index(self.left)] = lVariable
            self.left = lVariable
            return self
        elif not lVariable and rVariable:
            self.children[self.children.index(self.right)] = rVariable
            self.right = rVariable
            return self

        newVariable = LiteralNode()
        lValue = lVariable.convertValType()
        rValue = rVariable.convertValType()
        newType = getHighestOrder(lVariable.literalType, rVariable.literalType)
        if newType != "int" and newType != "float":
            newType = "int"
        newVariable.literalType = newType

        if self.operation == "+":
            newVariable.value = str(lValue + rValue)
        elif self.operation == "-":
            newVariable.value = str(lValue - rValue)

        return newVariable

    def generateLlvm(self, llvm):
        return llvm.visitTerm(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitTerm(self)

    def __repr__(self):
        return self.operation


class FactorNode(Node):
    type = "factor"
    operation = ""
    left = None
    right = None
    variableType = ""

    def checkOperationsValidity(self, table):
        lType = self.left.checkOperationsValidity(table)
        rType = self.right.checkOperationsValidity(table)
        return getHighestOrder(lType, rType)

    def constantFolding(self):
        lVariable = self.left.constantFolding()
        rVariable = self.right.constantFolding()
        if not lVariable and not rVariable:
            return False
        elif lVariable and not rVariable:
            self.children[self.children.index(self.left)] = lVariable
            self.left = lVariable
            return self
        elif not lVariable and rVariable:
            self.children[self.children.index(self.right)] = rVariable
            self.right = rVariable
            return self

        newVariable = LiteralNode()
        lValue = lVariable.convertValType()
        rValue = rVariable.convertValType()
        newType = getHighestOrder(lVariable.literalType, rVariable.literalType)
        if newType != "int" and newType != "float":
            newType = "int"
        newVariable.literalType = newType

        if self.operation == "*":
            newVariable.value = str(lValue * rValue)
        elif self.operation == "/":
            newVariable.value = str(lValue / rValue)
        elif self.operation == "%":
            newVariable.value = str(lValue % rValue)

        if newType == "int":
            newVariable.value = str(int(newVariable.value))

        return newVariable

    def generateLlvm(self, llvm):
        return llvm.visitFactor(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitFactor(self)

    def __repr__(self):
        return self.operation


class TypeCastNode(Node):
    type = "cast"
    castTo = ""
    variable = None

    def checkOperationsValidity(self, table):
        variableType = self.variable.checkOperationsValidity(table)
        if variableType == "address" or "*" in variableType or "[]" in variableType:
            raise Exception(f"Cannot cast {variableType} to {self.castTo}")
        return self.castTo

    def constantFolding(self):
        variable = self.variable.constantFolding()
        if not variable:
            return False
        elif variable.literalType == self.castTo:
            return variable

        value = variable.convertValType()
        if self.castTo == "float" or self.castTo == "int":
            variable.value = str(value + 0)
        elif self.castTo == "char":
            variable.value = chr(value + 0)
        elif self.castTo == "bool":
            if value:
                variable.value = "true"
            else:
                variable.value = "false"

        variable.literalType = self.castTo
        return variable

    def generateLlvm(self, llvm):
        return llvm.visitTypeCast(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitTypeCast(self)

    def __repr__(self):
        return '(' + self.castTo + ')'


class UnaryNode(Node):
    type = "unary"
    operation = ""
    variable = None
    variableType = ""

    def checkOperationsValidity(self, table):
        variableType = self.variable.checkOperationsValidity(table)

        if self.operation == "*":
            if "*" not in variableType:
                raise Exception(f"Cannot dereference {variableType}")
            else:
                return variableType[:-1]
        elif self.operation == "&":
            return "address"
        elif "[]" in variableType:
            raise Exception(f"Cannot perform {self.operation} operation on {variableType} type!")
        elif self.operation == "!":
            return "bool"
        else:
            if variableType == "float":
                return "float"
            else:
                return "int"

    def constantFolding(self):
        variable = self.variable.constantFolding()
        if not variable:
            return False

        value = variable.convertValType()
        variable.literalType = "int"
        if self.operation == "-":
            variable.value = str(-value)
        elif self.operation == "+":
            variable.value = str(value)
        elif self.operation == "!":
            if value:
                variable.value = "0"
            else:
                variable.value = "1"
        elif self.operation == "&":
            raise Exception("Cannot dereference literals!")

        return variable

    def generateLlvm(self, llvm):
        return llvm.visitUnary(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitUnary(self)

    def __repr__(self):
        return self.operation


class SpecialUnaryNode(Node):
    type = "special_unary"
    operation = ""
    variable = None

    def constantFolding(self):
        variable = self.variable.constantFolding()
        if not variable:
            return False

        value = variable.convertValType()
        if self.operation == "--":
            if variable.literalType == "char":
                variable.value = chr(ord(value[1:-1]) - 1)
            elif variable.literalType == "bool":
                variable.value = "false"
            else:
                variable.value = str(value - 1)
        elif self.operation == "++":
            if variable.literalType == "char":
                variable.value = chr(ord(value[1:-1]) + 1)
            elif variable.literalType == "bool":
                variable.value = "true"
            else:
                variable.value = str(value + 1)

        return variable

    def checkOperationsValidity(self, table):
        variableType = self.variable.checkOperationsValidity(table)
        if variableType == "float" or variableType == "int" or variableType == "char" or variableType == "bool":
            return variableType
        else:
            raise Exception(f"Cannot perform {self.operation} operation on {variableType}")

    def generateLlvm(self, llvm):
        return llvm.visitSpecialUnary(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitSpecialUnary(self)

    def __repr__(self):
        return self.operation


class LiteralNode(Node):
    type = "literal"
    literalType = ""
    value = ""

    def constantFolding(self):
        return self

    def convertValType(self):
        val = self.value
        if self.literalType == "float":
            val = float(val)
        elif self.literalType == "int":
            val = int(val)
        elif self.literalType == "char":
            val = val[1:-1]
        elif self.literalType == "bool":
            if val == "true" or val == "True":
                val = True
            else:
                val = False
        return val

    def checkOperationsValidity(self, table):
        return self.literalType

    def generateLlvm(self, llvm):
        return llvm.visitLiteral(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitLiteral(self, global_var)

    def __repr__(self):
        return self.value
