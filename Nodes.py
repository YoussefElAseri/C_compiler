import struct


class Node:
    children = []
    type = None
    line_nr: int = -100

    def __init__(self):
        self.children = []

    def addNodes(self, nodes):
        self.children.append(nodes)

    def foldConstant(self):
        return None

    def getASTvalue(self):
        return self.type

    def generateLlvm(self, llvm):
        pass

    def generateMips(self, mips, global_var=False):
        pass


class RunNode(Node):
    type = "run"
    include = False

    def generateLlvm(self, llvm):
        return llvm.visitRun(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitRun(self)


class IncludeNode(Node):
    type = "include"
    lib = "stdio"


class FuncDeclareNode(Node):
    type = "function_declaration"
    name = ""
    returnType = ""
    arguments = []

    def getASTvalue(self):
        return self.name


class FunctionNode(Node):
    type = "function"
    declaration = None  # FuncDeclareNode
    block = [] #BlockNode

    def generateMips(self, mips, global_var=False):
        a = mips.visitFunction(self)
        return a


class PrintfNode(Node):
    type = "printf"
    string = None # bv %d;
    arguments = [] #  : list[ArgumentNode]
    scope: list[int] = []

    def getASTvalue(self):
        return self.type

    def generateMips(self, mips, global_var=False):
        return mips.visitPrintf(self)


class ScanfNode(Node):
    type = "scanf"
    string = None
    arguments = []

    def generateMips(self, mips, global_var=False):
        return mips.visitScanf(self)

class FunctionArgNode(Node):
    type = "function_argument"
    const = None
    varType = None
    reference = None
    name = None

    def getASTvalue(self):
        if self.const:
            return "const " + self.varType
        else:
            return self.varType

class CallNode(Node):
    type = "call"
    name = ""
    arguments = []

    def getASTvalue(self):
        return self.name + "()"

    def generateMips(self, mips, global_var=False):
        return mips.visitFunction_call(self)


class ArgumentNode(Node):
    type = "argument"
    value = None


class BreakNode(Node):
    type = "break"

    def generateLlvm(self, llvm):
        return llvm.visitBreak(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitBreak(self)


class ContinueNode(Node):
    type = "continue"

    def generateLlvm(self, llvm):
        return llvm.visitContinue(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitContinue(self)


class ReturnNode(Node):
    type = "return"
    returnValue = None

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

    def getASTvalue(self):
        if type(self.returnValue) == str:
            return self.type + " " + self.returnValue
        elif self.returnValue.type == "term":
            return self.type + " " + str(self.returnValue.operation)
        elif self.returnValue.type == "variable":
            return self.type + " " + str(self.returnValue.name)
        elif self.returnValue.type == "factor":
            return self.type + " " + str(self.convert(self.returnValue.left)) \
                + str(self.returnValue.operation) + str(self.convert(self.returnValue.right))
        elif self.returnValue.type == "call":
            return self.type + " " + str(self.returnValue.name) + str(self.getargs(self.returnValue.arguments))
        elif self.returnValue.type == "literal":
            return self.type + " " + str(self.returnValue.value)
        else:
            print("error147")

    def generateMips(self, mips, global_var=False):
        return mips.visitReturn(self)


class BlockNode(Node):
    type = "block"
    # all code inside
    block = None
    comment = ""

    def generateLlvm(self, llvm):
        for i in self.children:
            i.generateLlvm(llvm)

    def generateMips(self, mips, global_var=False):
        mips.visitBlock(self)


class StatementNode(Node):
    # Een statementNode heeft altijd maximum 1 kind
    type = "line"
    statement = None
    comment = None
    instruction = ""

    def generateLlvm(self, llvm):
        return llvm.visitLine(self)

    def generateMips(self, mips, global_var=False):
        if self.comment:
            self.comment.generateMips(mips)
        if self.statement:
            mips.text.append("")
            instr = self.instruction
            instr = instr.split("\n")
            for i in instr:
                mips.text.append("# " + i)
            self.statement.generateMips(mips)


class IfNode(Node):
    type = "if"
    condition = None
    # all code inside
    block = None
    elseNode = None
    comment = None

    def generateLlvm(self, llvm):
        return llvm.visitIf(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitIf(self)


class ElseNode(Node):
    type = "else"
    # all code inside
    block = None

    def generateLlvm(self, llvm):
        return llvm.visitElse(self)

    def generateMips(self, mips, global_var=False):
        mips.visitBlock(self.block)


class WhileNode(Node):
    type = "while"
    condition = None
    block = None
    comment = None

    def generateLlvm(self, llvm):
        return llvm.visitWhile(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitWhile(self)


class ExpressionStatementNode(Node):
    type = "statement"
    instruction = ""  # str

    def getASTvalue(self):
        return self.instruction

    def generateLlvm(self, llvm):
        return llvm.visitExpressionStatement(self)

    def generateMips(self, mips, global_var=False):
        mips.text.append(f"\n ## {self.instruction}")
        return mips.visitExpressionStatement(self)


class CommentNode(Node):
    type = "comment"
    text = ""

    def getASTvalue(self):
        return self.text

    def generateLlvm(self, llvm):
        return llvm.visitComment(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitComment(self)


class AssignmentNode(Node):
    type = "assignment"
    left = None
    right = None
    scope: list[int] = []

    def generateLlvm(self, llvm):
        return llvm.visitAssignment(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitAssignment(self, global_var)


class InstantiationNode(Node):
    type = "instantiation"
    const = False
    varType = ""  # type int, float, ...
    name = ""  # variable name x, y , ...

    def getASTvalue(self):
        return str(self.name)

    def generateLlvm(self, llvm):
        return llvm.visitInstantiation(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitInstantiation(self, global_var)


class VariableNode(Node):
    type = "variable"
    name = ""

    def getASTvalue(self):
        return str(self.name)

    def generateLlvm(self, llvm):
        return llvm.visitVariable(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitVariable(self)


class ArrayInstantiationNode(Node):
    type = "arrayInstantiation"
    name = ""
    size = None
    varType = ""
    const = ""

    def generateMips(self, mips, global_var=False):
        return mips.visitArrayInstantiation(self, global_var)


class ArrayNode(Node):
    type = "array"
    name = ""
    index = None

    def generateMips(self, mips, global_var=False):
        return mips.visitArray(self)


class LogicNode(Node):
    type = "logic"
    operation = ""
    left = None
    right = None

    def foldConstant(self):
        if self.left.type == "literal" and self.right.type == "literal":
            node = LiteralNode()
            leftVal = self.left.convertValType()
            rightVal = self.right.convertValType()
            node.literalType = "bool"

            if self.operation == "&&":
                node.value = str(leftVal and rightVal)
            elif self.operation == "||":
                node.value = str(leftVal or rightVal)
            return node
        return None

    def generateLlvm(self, llvm):
        return llvm.visitLogic(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitLogic(self)


class CompareNode(Node):
    type = "compare"
    operation = ""
    left = None
    right = None

    def foldConstant(self):
        if self.left.type == "literal" and self.right.type == "literal":
            node = LiteralNode()
            leftVal = self.left.convertValType()
            rightVal = self.right.convertValType()
            node.literalType = "bool"
            if self.operation == "<":
                node.value = str(leftVal < rightVal)
            elif self.operation == "<=":
                node.value = str(leftVal <= rightVal)
            elif self.operation == "==":
                node.value = str(leftVal == rightVal)
            elif self.operation == "!=":
                node.value = str(leftVal != rightVal)
            elif self.operation == ">=":
                node.value = str(leftVal >= rightVal)
            elif self.operation == ">":
                node.value = str(leftVal > rightVal)
            return node
        return None

    def generateLlvm(self, llvm):
        return llvm.visitCompare(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitCompare(self)


class TermNode(Node):
    type = "term"
    operation = ""
    left = None
    right = None

    def getASTvalue(self):
        return str(self.operation)

    def foldConstant(self):
        if self.left.type == "literal" and self.right.type == "literal":
            node = LiteralNode()
            leftVal = self.left.convertValType()
            rightVal = self.right.convertValType()
            Ltype = self.left.literalType
            Rtype = self.right.literalType
            if Ltype == "float" or Rtype == "float":
                node.literalType = "float"
            else:
                node.literalType = "int"
            if Ltype == "char":
                leftVal = ord(leftVal[1:-1])
            if Rtype == "char":
                temp = rightVal[1:-1]
                rightVal = ord(temp)

            if self.operation == "+":
                node.value = str(leftVal + rightVal)
            elif self.operation == "-":
                node.value = str(leftVal - rightVal)
            return node
        return None

    def generateLlvm(self, llvm):
        return llvm.visitTerm(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitTerm(self)


class FactorNode(Node):
    type = "factor"
    operation = ""
    left = None
    right = None

    def getASTvalue(self):
        return str(self.operation)

    def foldConstant(self):
        if self.left.type == "literal" and self.right.type == "literal":
            node = LiteralNode()
            leftVal = self.left.convertValType()
            rightVal = self.right.convertValType()
            Ltype = self.left.literalType
            Rtype = self.right.literalType
            if Ltype == "float" or Rtype == "float":
                node.literalType = "float"
            else:
                node.literalType = "int"
            if Ltype == "char":
                leftVal = ord(leftVal[1:-1])
            if Rtype == "char":
                temp = rightVal[1:-1]
                rightVal = ord(temp)

            if self.operation == "*":
                node.value = str(leftVal * rightVal)
            elif self.operation == "/":
                if not (leftVal/rightVal).is_integer():
                    node.literalType = "float"
                    node.value = str(leftVal / rightVal)
                else:
                    node.value = str(int(leftVal / rightVal))

            elif self.operation == "%":
                node.value = str(leftVal % rightVal)
            return node
        return None

    def generateLlvm(self, llvm):
        return llvm.visitFactor(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitFactor(self)


class TypeCastNode(Node):
    type = "cast"
    castTo = ""
    variable = None

    def generateLlvm(self, llvm):
        return llvm.visitTypeCast(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitTypeCast(self)


class UnaryNode(Node):
    type = "unary"
    operation = ""
    variable = None

    def getASTvalue(self):
        return str(self.operation)

    def foldConstant(self):
        if self.variable.type == "literal":
            node = LiteralNode()
            val = self.variable.convertValType()
            valType = self.variable.literalType
            if valType == "float":
                node.literalType = "float"
            else:
                node.literalType = "int"
            if valType == "char":
                val = ord(val[1:-1])
            if self.operation == "-":
                node.value = str(-val)
            elif self.operation == "+":
                node.value = str(val)
            elif self.operation == "!":
                node.literalType = "bool"
                node.value = str(not val)
            elif self.operation == "&":
                return None
            return node
        return None

    def generateLlvm(self, llvm):
        return llvm.visitUnary(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitUnary(self)


class SpecialUnaryNode(Node):
    type = "special_unary"
    operation = ""
    variable = None

    def getASTvalue(self):
        if self.variable.type == "unary":
            n = self.variable.variable.name
        else:
            n = self.variable.name
        return n + self.operation

    def foldConstant(self):
        if self.variable.type == "literal":
            node = LiteralNode()
            val = self.variable.convertValType()
            valType = self.variable.literalType
            if valType == "bool":
                raise Exception(f"Invalid operation on boolean type")
            elif valType == "float":
                node.literalType = "float"
            else:
                node.literalType = "int"
            if valType == "char":
                val = ord(val[1:-1])
            if self.operation == "--":
                node.value = str(val-1)
            elif self.operation == "++":
                node.value = str(val+1)
            return node
        return None

    def generateLlvm(self, llvm):
        return llvm.visitSpecialUnary(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitSpecialUnary(self)


class LiteralNode(Node):
    type = "literal"
    literalType = ""
    value = ""

    def getASTvalue(self):
        return str(self.value)

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

    def generateLlvm(self, llvm):
        return llvm.visitLiteral(self)

    def generateMips(self, mips, global_var=False):
        return mips.visitLiteral(self, global_var)
