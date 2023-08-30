from AST import AST
from Antlr.CVisitor import *
from Antlr.CParser import *
from Nodes import *
from SymbolTable import SymbolTable, Contexts


class AstVisitor(CVisitor):
    def __init__(self):
        self.symbolTable: SymbolTable = SymbolTable()
        self.currentTable: SymbolTable = self.symbolTable
        self.contexts = Contexts()

    def visitRun(self, ctx: CParser.RunContext):
        if ctx.exception is not None:
            # Wrs include en niet int main()
            raise Exception("Syntax error: Int Main() Not found!")

        ast = AST()
        node = RunNode()
        if ctx.include():
            self.visitInclude(ctx.include())
            node.include = True
        for child in ctx.children:
            if isinstance(child, CParser.FunctionContext):
                node.children.append(self.visitFunction(child))
            elif isinstance(child, CParser.Global_varContext):
                node.children.extend(self.visitGlobal_var(child))
            elif isinstance(child, CParser.Forward_declareContext):
                node.children.append(self.visitForward_declare(child))
            elif isinstance(child, CParser.CommentContext):
                node.children.append(self.visitComment(child))

        for entry in self.symbolTable.scope:
            tempDict = self.symbolTable.scope[entry]
            if tempDict["type"] == "function" and tempDict["calls"] > 0 and tempDict["definition"] is False:
                raise Exception("Function was called but not defined!")

        ast.root = node
        ast.symbolTable = self.symbolTable
        return ast

    def visitInclude(self, ctx: CParser.IncludeContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        # TODO: support ... ?

        self.symbolTable.addFunctionEntry("printf", True, "void", "...")
        self.symbolTable.addFunctionEntry("scanf", True, "void", "...")

    def visitGlobal_var(self, ctx: CParser.Global_varContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        nodes = []
        if ctx.instantiationExpression():
            nodes = self.visitInstantiationExpression(ctx.instantiationExpression())
        elif ctx.array_initialisation():
            nodes = [self.visitArray_initialisation(ctx.array_initialisation())]

        return nodes

    def visitInstantiationExpression(self, ctx: CParser.InstantiationExpressionContext):
        nodes = []
        isConst = False
        if ctx.CONST():
            isConst = True

        for i in range(0, len(ctx.COMMA()) + 1):
            if isConst:
                temp = self.visitConst(ctx.const(i))
            else:
                temp = self.visitNot_const(ctx.not_const(i))

            newNode = InstantiationNode()
            newNode.const = isConst
            newNode.varType = ctx.type_().getText()
            newNode.name = temp[0]

            self.currentTable.addVariableEntry(newNode.name, newNode.varType, newNode.const)

            if temp[1]:
                assignmentNode = AssignmentNode()
                assignmentNode.left = newNode
                assignmentNode.right = temp[1]
                assignmentNode.children = [newNode, temp[1]]
                nodes.append(assignmentNode)
                self.currentTable.addAssignment(newNode.name)
            else:
                nodes.append(newNode)

        return nodes

    def visitNot_const(self, ctx: CParser.Not_constContext):
        if ctx.EQUALS():
            return ctx.IDENTIFIER().getText(), self.visitLogicexpression(ctx.logicexpression())
        return ctx.IDENTIFIER().getText(), None

    def visitConst(self, ctx: CParser.ConstContext):
        return ctx.IDENTIFIER().getText(), self.visitLogicexpression(ctx.logicexpression())

    def visitFunction_declaration(self, ctx: CParser.Function_declarationContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = FuncDeclareNode()
        if ctx.VOID():
            node.returnType = "void"
        elif ctx.type_():
            node.returnType = ctx.type_().getText()
        node.name = ctx.IDENTIFIER().getText()
        if ctx.argument_declaration():
            node.arguments = self.visitArgument_declaration(ctx.argument_declaration())
            node.children = node.arguments

        self.currentTable.addFunctionEntry(node.name, False, node.returnType, node.arguments)

        return node

    def visitArgument_declaration(self, ctx: CParser.Argument_declarationContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = FunctionArgNode()
        if ctx.CONST():
            node.const = True
        node.varType = ctx.type_().getText()
        node.name = ctx.IDENTIFIER().getText()

        if ctx.COMMA():
            allArgs = self.visitArgument_declaration(ctx.argument_declaration()).insert(0, node)
            return allArgs

        return [node]

    def visitForward_declare(self, ctx: CParser.Forward_declareContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = FunctionNode()
        node.declaration = self.visitFunction_declaration(ctx.function_declaration())
        node.children = [node.declaration]

        return node

    def visitFunction(self, ctx: CParser.FunctionContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = FunctionNode()
        node.declaration = self.visitFunction_declaration(ctx.function_declaration())
        node.name = node.declaration.name
        self.currentTable.retrieveEntry(node.declaration.name)[0]["definition"] = True

        # Add function context
        self.contexts.pushFunction(node.declaration.name, node.declaration.returnType)

        # Add all arguments to the symbolTable
        self.currentTable = self.currentTable.openScope()
        for argument in node.declaration.arguments:
            self.currentTable.addVariableEntry(argument.name, argument.varType, argument.const)

        node.block = self.visitBlock_scope(ctx.block_scope(), True)

        # Pop function context
        self.contexts.popFunction()

        node.children = [node.declaration, node.block]
        return node

    def visitBlock_scope(self, ctx: CParser.Block_scopeContext, openedScope=False):
        if ctx.exception is not None:
            raise Exception("syntax error")

        if not openedScope:
            self.currentTable = self.currentTable.openScope()

        node = BlockNode()
        nodes = []
        statements = ctx.statement()
        for statement in statements:
            temp = self.visitStatement(statement)
            if isinstance(temp, tuple):
                for t in temp:
                    nodes.append(t)
            else:
                if temp.type == "break" or temp.type == "continue":
                    break
                nodes.append(temp)
        node.children = nodes

        self.currentTable = self.currentTable.closeScope()

        return node

    def visitStatement(self, ctx: CParser.StatementContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = None
        if ctx.expression_statement():
            node = StatementNode()
            node.statement = self.visitExpression_statement(ctx.expression_statement())
            node.children.append(node.statement)
        elif ctx.array_initialisation():
            node = StatementNode()
            node.statement = self.visitArray_initialisation(ctx.array_initialisation())
            node.children.append(node.statement)
        elif ctx.jump_statement():
            node = StatementNode()
            node.statement = self.visitJump_statement(ctx.jump_statement())
            node.children.append(node.statement)
        elif ctx.compound_statement():
            node = self.visitCompound_statement(ctx.compound_statement())
            # Case where for is turned into while
            if isinstance(node, tuple):
                whileNode = node[1]
                node = node[0]
                node.instruction = ctx.getText()

                if ctx.comment():
                    node.comment = self.visitComment(ctx.comment())
                    node.children.append(node.comment)
                return node, whileNode
        elif ctx.block_scope():
            node = BlockNode()
            node.block = self.visitBlock_scope(ctx.block_scope())
            node.children.append(node.block)

        if ctx.comment() and node is None:
            node = self.visitComment(ctx.comment())
        elif ctx.comment():
            node.comment = self.visitComment(ctx.comment())
            node.children.append(node.comment)
        node.instruction = ctx.getText()
        return node

    def visitArray_initialisation(self, ctx: CParser.Array_initialisationContext):
        if ctx.exception is not None:
            raise Exception("syntax error; Invalid index into Array.")

        node = ArrayInstantiationNode()
        node.name = ctx.IDENTIFIER().getText()
        node.size = int(ctx.INTLITERAL().getText())
        node.varType = ctx.type_().getText()

        # Add to Symbol Table
        self.currentTable.addArrayEntry(node.name, node.varType)
        return node

    def visitArray(self, ctx: CParser.ArrayContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = ArrayNode()
        node.name = ctx.IDENTIFIER().getText()
        node.index = self.visitLogicexpression(ctx.logicexpression())

        self.currentTable.checkEntry(node.name, "Array")

        node.variableType = self.currentTable.retrieveEntry(node.name)[0]["variableType"]

        return node

    def visitFunction_call(self, ctx: CParser.Function_callContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        if ctx.scanf():
            node = self.visitScanf(ctx.scanf())
            return node
        elif ctx.printf():
            node = self.visitPrintf(ctx.printf())
            return node

        node = CallNode()
        node.name = ctx.IDENTIFIER().getText()

        self.currentTable.checkEntry(node.name, "Function")

        if ctx.argument():
            node.arguments = self.visitArgument(ctx.argument())
            node.children = node.arguments

        self.currentTable.addCall(node.name)

        return node

    def visitScanf(self, ctx: CParser.ScanfContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        self.currentTable.checkEntry("scanf", "Function")

        node = ScanfNode()
        node.string = ctx.STRINGLITERAL().getText()[1:-1]
        if ctx.argument():
            node.arguments = self.visitArgument(ctx.argument())

        node.children = node.arguments

        self.currentTable.addCall("scanf")

        return node

    def visitPrintf(self, ctx: CParser.PrintfContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        self.currentTable.checkEntry("printf", "Function")

        node = PrintfNode()
        node.string = ctx.STRINGLITERAL().getText()[1:-1]

        if ctx.argument():
            node.arguments = self.visitArgument(ctx.argument())

        node.children = node.arguments

        self.currentTable.addCall("printf")

        return node

    def visitArgument(self, ctx: CParser.ArgumentContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = ArgumentNode()
        if ctx.logicexpression():
            node.value = self.visitLogicexpression(ctx.logicexpression())
        else:
            node.value = ctx.STRINGLITERAL().getText()

        node.children = [node.value]

        if ctx.COMMA():
            allArgs = [node]
            arguments = self.visitArgument(ctx.argument())
            for arg in arguments:
                allArgs.append(arg)
            return allArgs
        return [node]

    def visitJump_statement(self, ctx: CParser.Jump_statementContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = None
        if ctx.break_():
            node = BreakNode()
            node.context = self.contexts.peekLoop()
        elif ctx.continue_():
            node = ContinueNode()
            node.context = self.contexts.peekLoop()
        elif ctx.return_():
            node = ReturnNode()
            if ctx.logicexpression():
                node.returnValue = self.visitLogicexpression(ctx.logicexpression())
                node.children = [node.returnValue]
            else:
                node.returnValue = "void"
            node.context = self.contexts.peekFunction()[0]
            node.returnType = self.contexts.peekFunction()[1]

        return node

    def visitCompound_statement(self, ctx: CParser.Compound_statementContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = None
        if ctx.if_():
            node = self.visitIf(ctx.if_())
        elif ctx.while_():
            node = self.visitWhile(ctx.while_())
        elif ctx.for_():
            node = self.visitFor(ctx.for_())

        return node

    def visitIf(self, ctx: CParser.IfContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = IfNode()
        node.condition = self.visitCondition(ctx.condition())

        self.currentTable = self.currentTable.openScope()
        node.block = self.visitBlock_scope(ctx.block_scope())
        self.currentTable = self.currentTable.closeScope()

        node.children = [node.condition, node.block]
        if ctx.else_():
            node.elseNode = self.visitElse(ctx.else_())
            node.children.append(node.elseNode)

        return node

    def visitCondition(self, ctx: CParser.ConditionContext):
        return self.visitLogicexpression(ctx.logicexpression())

    def visitElse(self, ctx: CParser.ElseContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = ElseNode()

        self.currentTable = self.currentTable.openScope()
        node.block = self.visitBlock_scope(ctx.block_scope())
        self.currentTable = self.currentTable.closeScope()

        node.children = [node.block]

        return node

    def visitWhile(self, ctx: CParser.WhileContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = WhileNode()
        node.condition = self.visitCondition(ctx.condition())

        self.contexts.pushLoop()
        self.currentTable = self.currentTable.openScope()
        node.block = self.visitBlock_scope(ctx.block_scope())
        self.currentTable = self.currentTable.closeScope()
        self.contexts.popLoop()

        node.children = [node.condition, node.block]

        return node

    # returns two nodes instead of one
    def visitFor(self, ctx: CParser.ForContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        While = WhileNode()

        Statement = StatementNode()

        self.contexts.pushLoop()
        self.currentTable = self.currentTable.openScope()
        condition = self.visitFor_condition(ctx.for_condition())
        Statement.statement = condition[0]
        Statement.children = [Statement.statement]
        While.condition = condition[1]
        While.block = self.visitBlock_scope(ctx.block_scope())
        self.currentTable = self.currentTable.closeScope()
        self.contexts.popLoop()

        While.block.children.append(condition[2])
        While.children = [While.condition, While.block]

        return Statement, While

    def visitFor_condition(self, ctx: CParser.For_conditionContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        # changed assignment to assignment or instantiationExpression
        if ctx.assignment():
            temp = self.visitAssignment(ctx.assignment())
        else:
            temp = self.visitInstantiationExpression(ctx.instantiationExpression())[0]

        condition = [temp, self.visitLogicexpression(ctx.logicexpression()),
                     self.visitUpdate_expression(ctx.update_expression())]

        return condition

    def visitUpdate_expression(self, ctx: CParser.Update_expressionContext):
        if ctx.EQUALS():
            node = AssignmentNode()
            if ctx.IDENTIFIER():
                self.currentTable.checkEntry(ctx.getText(), "Variable")
                node.left = VariableNode()
                node.left.name = ctx.getText()
                self.currentTable.addAssignment(node.left.name)
            # No addAssignment for pointers
            elif ctx.pointer():
                node.left = self.visitPointer(ctx.pointer())
            node.right = self.visitLogicexpression(ctx.logicexpression())
            node.children = [node.left, node.right]
        else:
            return self.visitLogicexpression(ctx.logicexpression())

    def visitExpression_statement(self, ctx: CParser.Expression_statementContext):
        if ctx.exception is not None:
            print(ctx.exception)
            raise Exception("syntax error")

        node = ExpressionStatementNode()
        node.instruction = ctx.getText()
        if ctx.assignment():
            node.children = [self.visitAssignment(ctx.assignment())]
        elif ctx.logicexpression():
            node.children = [self.visitLogicexpression(ctx.logicexpression())]
        # added instantiationExpression
        elif ctx.instantiationExpression():
            node.children = self.visitInstantiationExpression(ctx.instantiationExpression())

        return node

    def visitComment(self, ctx: CParser.CommentContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = CommentNode()
        node.text = ctx.getText()
        return node

    def visitAssignment(self, ctx: CParser.AssignmentContext, loop: bool = False):
        if ctx.exception is not None:
            raise Exception("syntax error")
        if ctx.rvalue_assignment():
            raise Exception(f"Cannot assign rvalue {ctx.rvalue_assignment().logicexpression(0).getText()}!")

        node = AssignmentNode()
        if ctx.declaration():
            node.left = self.visitDeclaration(ctx.declaration())
            if ctx.declaration().IDENTIFIER():
                self.currentTable.addAssignment(node.left.name)

        node.right = self.visitLogicexpression(ctx.logicexpression())
        node.children = [node.left, node.right]

        return node

    def visitDeclaration(self, ctx: CParser.DeclarationContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = None
        if ctx.array():
            node = self.visitArray(ctx.array())
        elif ctx.IDENTIFIER():
            node = VariableNode()
            node.name = ctx.getText()
        elif ctx.pointer():
            node = self.visitPointer(ctx.pointer())

        return node

    def visitType(self, ctx: CParser.TypeContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        return ctx.getText()

    def visitLogicexpression(self, ctx: CParser.LogicexpressionContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        if not ctx.logicops():
            node = self.visitBoolexpression(ctx.boolexpression(0))
            return node
        node = LogicNode()
        node.operation = ctx.logicops().getText()
        node.left = self.visitBoolexpression(ctx.boolexpression(0))
        if ctx.logicexpression():
            node.right = self.visitLogicexpression(ctx.logicexpression())
        else:
            node.right = self.visitBoolexpression(ctx.boolexpression(1))
        node.children = [node.left, node.right]
        return node

    def visitBoolexpression(self, ctx: CParser.BoolexpressionContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        if not ctx.compops():
            node = self.visitTerm(ctx.term(0))
            return node
        if not ctx.boolexpression():
            node = CompareNode()
            node.operation = ctx.compops().getText()
            node.left = self.visitTerm(ctx.term(0))
            node.right = self.visitTerm(ctx.term(1))
            node.children = [node.left, node.right]
            return node

        node = LogicNode()
        node.operation = "&&"
        compNode1 = CompareNode()
        compNode1.operation = ctx.compops().getText()
        compNode2 = self.visitBoolexpression(ctx.boolexpression())
        compNode1.left = self.visitTerm(ctx.term(0))
        compNode1.right = compNode2.left
        node.left = compNode1
        node.right = compNode2
        node.children = [node.left, node.right]

        return node

    def visitTerm(self, ctx: CParser.TermContext):
        if ctx.exception is not None:
            raise Exception("syntax error")
        if not ctx.termops():
            node = self.visitFactor(ctx.factor(0))
            return node
        node = TermNode()
        node.operation = ctx.termops().getText()
        node.left = self.visitFactor(ctx.factor(0))

        if ctx.term():
            node.right = self.visitTerm(ctx.term())
        else:
            node.right = self.visitFactor(ctx.factor(1))
        node.children = [node.left, node.right]

        return node

    def visitFactor(self, ctx: CParser.FactorContext):
        if ctx.exception is not None:
            raise Exception("syntax error")
        if not ctx.factorops():
            node = self.visitElement(ctx.element(0))
            return node
        node = FactorNode()
        node.operation = ctx.factorops().getText()
        node.left = self.visitElement(ctx.element(0))
        if ctx.factor():
            node.right = self.visitFactor(ctx.factor())
        else:
            node.right = self.visitElement(ctx.element(1))
        node.children = [node.left, node.right]
        return node

    def visitElement(self, ctx: CParser.ElementContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = None
        if ctx.typecast():
            node = TypeCastNode()
            node.castTo = ctx.typecast().getText()[1:-1]
            node.variable = self.visitElement(ctx.element())
            node.children = [node.variable]
        elif ctx.unaryops():
            node = UnaryNode()
            node.operation = ctx.unaryops().getText()
            node.variable = self.visitElement(ctx.element())
            if node.variable.type == "literal" and node.operation == "&":
                raise Exception(f"Cannot dereference literals!")
            node.children = [node.variable]
        elif ctx.literal():
            node = self.visitLiteral(ctx.literal())
        elif ctx.pointer():
            node = self.visitPointer(ctx.pointer())
        elif ctx.IDENTIFIER():
            node = VariableNode()
            node.name = ctx.IDENTIFIER().getText()
            self.currentTable.checkEntry(node.name, "Variable")
            self.currentTable.addUse(node.name)
        elif ctx.array():
            node = self.visitArray(ctx.array())
            self.currentTable.addUse(node.name)
        elif ctx.logicexpression():
            node = self.visitLogicexpression(ctx.logicexpression())
        elif ctx.function_call():
            node = self.visitFunction_call(ctx.function_call())

        if ctx.SPECIALUNARY():
            newNode = SpecialUnaryNode()
            newNode.operation = ctx.SPECIALUNARY().getText()
            newNode.variable = node
            newNode.children = [newNode.variable]
            node = newNode

        return node

    def visitPointer(self, ctx: CParser.PointerContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = UnaryNode()
        node.operation = ctx.STAR().getText()
        variable = None
        if ctx.IDENTIFIER():
            variable = VariableNode()
            variable.name = ctx.IDENTIFIER().getText()
            self.currentTable.addUse(variable.name)
            self.currentTable.checkEntry(variable.name, "Variable")
        elif ctx.pointer():
            variable = self.visitPointer(ctx.pointer())
        node.variable = variable

        return node

    def visitLiteral(self, ctx: CParser.LiteralContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = LiteralNode()
        node.value = ctx.getText()

        if ctx.BOOLLITERAL():
            node.literalType = 'bool'
        elif ctx.INTLITERAL():
            node.literalType = 'int'
        elif ctx.FLOATLITERAL():
            node.literalType = 'float'
        elif ctx.CHARLITERAL():
            if "\\" in node.value:
                node.value = eval('"' + node.value + '"')
            node.literalType = 'char'

        return node
