from Antlr.CVisitor import *
from Antlr.CParser import *
from Nodes import *
from AST import AST
from SymbolTable import SymbolTable


class AstVisitor(CVisitor):
    def __init__(self):
        self.symbol_table: SymbolTable = SymbolTable([0])
        self.cur_symbol_table: SymbolTable = self.symbol_table
        self.functions: list[(FuncDeclareNode,bool)] = [] # de bool om aan te duiden of het al gedefinieerd is
        self.line_nr: int = -30
        self.loop = False
        #self.declarations  = None

    def visitRun(self, ctx: CParser.RunContext):
        if ctx.exception is not None:
            raise Exception("Syntax error: Int Main() Not found!")

        ast = AST()
        node = RunNode()
        self.line_nr = 0
        if ctx.include():
            #self.line_nr += 1
            self.visitInclude(ctx.include())
            #print(ctx.include().getText())
            node.include = True
        for child in ctx.children:
            self.line_nr += 1
            if isinstance(child, CParser.FunctionContext):
                node.children.append(self.visitFunction(child))
            elif isinstance(child, CParser.Global_varContext):
                node.children.extend(self.visitGlobal_var(child))
                #node.children.append(self.visitGlobal_var(child))
            elif isinstance(child, CParser.Forward_declareContext):
                node.children.append(self.visitForward_declare(child))
            elif isinstance(child, CParser.CommentContext):
                node.children.append(self.visitComment(child))
        ast.root = node
        ast.symbol_table = self.symbol_table
        return ast

    def visitInclude(self, ctx:CParser.IncludeContext):
        if ctx.exception is not None:
            raise Exception("syntax error")



    def visitGlobal_var(self, ctx: CParser.Global_varContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        nodes = []
        # added array initialisation
        if ctx.instantiationExpression():
            nodes = self.visitInstantiationExpression(ctx.instantiationExpression())
        elif ctx.array_initialisation():
            nodes = [self.visitArray_initialisation(ctx.array_initialisation())]

        # is a list
        return nodes

    def semantic_rede_check(self, node: InstantiationNode, isConst: bool, is_array: bool = False):
        # (Checking for) Redeclaration or redefinition of an existing variable
        # Also adds the node to the symbol table if everything checks out

        if isConst:
            self.cur_symbol_table.add_symbol(str(node.name), "const" + str(node.varType))
        else:
            if is_array:
                self.cur_symbol_table.add_symbol(str(node.name), "array"+str(node.varType))
            else:
                self.cur_symbol_table.add_symbol(str(node.name), str(node.varType))


    def visitInstantiationExpression(self, ctx: CParser.InstantiationExpressionContext, loop:bool = False):
        nodes = []
        isConst = False
        if ctx.CONST():
            isConst = True

        if isConst:
            temp = self.visitConst(ctx.const(0))
        else:
            temp = self.visitNot_const(ctx.not_const(0))
        firstNode = InstantiationNode()
        firstNode.const = isConst
        firstNode.varType = ctx.type_().getText()
        firstNode.name = temp[0]
        self.semantic_rede_check(firstNode, isConst)

        if temp[1]:
            assignmentNode = AssignmentNode()
            assignmentNode.scope = self.cur_symbol_table.name
            assignmentNode.left = firstNode
            assignmentNode.right = temp[1]
            assignmentNode.children = [firstNode, temp[1]]
            nodes.append(assignmentNode)
            self.semantic_assignment_check(assignmentNode)
        else:
            nodes.append(firstNode)
        for i in range(1,len(ctx.COMMA())+1):
            newNode = InstantiationNode()
            newNode.const = isConst
            newNode.varType = ctx.type_().getText()
            if isConst:
                temp = self.visitConst(ctx.const(i))
            else:
                temp = self.visitNot_const(ctx.not_const(i))
            newNode.name = temp[0]
            self.semantic_rede_check(newNode, isConst)

            if temp[1]:
                assignmentNode = AssignmentNode()
                assignmentNode.scope = self.cur_symbol_table.name
                assignmentNode.left = newNode
                assignmentNode.right = temp[1]
                assignmentNode.children = [newNode, temp[1]]
                nodes.append(assignmentNode)

                self.semantic_assignment_check(assignmentNode)
            else:
                nodes.append(newNode)


        return nodes

    def visitNot_const(self, ctx: CParser.Not_constContext):
        if ctx.EQUALS():
            return ctx.IDENTIFIER(), self.visitLogicexpression(ctx.logicexpression())
        return ctx.IDENTIFIER(), None

    def visitConst(self, ctx: CParser.ConstContext):
        return ctx.IDENTIFIER(), self.visitLogicexpression(ctx.logicexpression())

    def append_arguments(self, args:list[FunctionArgNode]):
        list_args = []
        for arg in args:
            new_arg: str = ""
            if arg.const:
                new_arg += "const"
            if arg.reference:
                new_arg += "*"
            if arg.varType:
                new_arg += arg.varType
            list_args.append(new_arg)

        return list_args

    def semantic_function_check(self, node: FuncDeclareNode):
        nrt = node.returnType
        for f in self.functions:
            frt = f[0].returnType
            if f[0].name == node.name:
                # 2 functies met dezelfde naam -> alle attributen moeten hetzelfde zijn

                # 1) Returntype checken
                if frt != nrt:
                    raise Exception(f"Semantic error: Conflicting return type for '{node.name}'; "
                                    f"declared '{frt}' return type, but previously declared '{nrt}' return type.")

                # 2) Arguments checken
                fa: list[str] = self.append_arguments(f[0].arguments)
                na: list[str] = self.append_arguments(node.arguments)
                fal = len(fa)


                if len(na) != fal:
                    raise Exception(f"Semantic error: Conflicting parameters for '{node.name}';"
                                    f"has {na}, but previously declared {fa}")

                for i in range(0,fal):
                    if fa[i] != na[i]:
                        raise Exception(f"Semantic error: Conflicting parameters for '{node.name}'; "
                                        f"has {na}, but previously declared {fa}")
                    """if f.arguments[i].const != node.arguments[i].const:
                        raise Exception(f"Semantic error: Conflicting parameter type for '{node.name}'; "
                                        f"conflicting parameter attribute: reference.")
                    elif f.arguments[i].varType != node.arguments[i].varType:
                        raise Exception(f"Semantic error: Conflicting return type for '{node.name}'; "
                                        f"conflicting parameter attribute: reference.")
                    elif f.arguments[i].reference != node.arguments[i].reference:
                        print(node.arguments[i].reference)
                        raise Exception(f"Semantic error: Conflicting return type for '{node.name}'; "
                                        f"conflicting parameter attribute: reference.")"""




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

        self.semantic_function_check(node)
        # Toevoegen aan functie lijst
        t: tuple[FuncDeclareNode, bool] = (node,False)
        self.functions.append(t)
        return node

    def visitArgument_declaration(self, ctx: CParser.Argument_declarationContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = FunctionArgNode()
        if ctx.CONST():
            node.const = True
        if ctx.AMPERSAND():
            node.reference = True
        node.varType = ctx.type_().getText()
        node.name = ctx.IDENTIFIER().getText()

        self.cur_symbol_table.add_symbol(node.name, node.varType, False)
        self.cur_symbol_table.add_symbol_value(node.name, 0, -100)

        if ctx.COMMA():
            allArgs = [node]
            arguments = self.visitArgument_declaration(ctx.argument_declaration())
            for arg in arguments:
                allArgs.append(arg)
            return allArgs

        return [node]


    def visitForward_declare(self, ctx:CParser.Forward_declareContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = FunctionNode()
        node.declaration = self.visitFunction_declaration(ctx.function_declaration())
        flag = False
        if node.declaration.name == "main":
            flag = True
        #node.block = self.visitBlock_scope(ctx.block_scope(), flag)
        node.children = [node.declaration]
        return node

    def find_returns(self, node: BlockNode) -> list[ReturnNode]:
        listrn: list[ReturnNode] = []
        # Find all return nodes in this block
        for child in node.children:
            if child.type == "if":
                listrn = listrn + self.find_returns(child.block)
                if child.elseNode:
                    listrn = listrn + self.find_returns(child.elseNode)

            if child.children:

                if child.children[0].type == "return":
                    listrn.append(child.children[0])
        return listrn

    def semantic_return_check(self, node):
        # Check the consistency of the return statement with the return type of the enclosing function.
        rt = node.declaration.returnType

        # Return_Node 's vinden in Block_Node
        listrn: list[ReturnNode] = self.find_returns(node.block)  # Return Node Value

        for rnv in listrn:
            s = rnv.scope
            rnv = rnv.returnValue

            if rnv == "void":
                pass
            elif rnv.type == "literal":
                rnv = rnv.literalType
            elif rnv.type == "variable":
                ##self.cur_symbol_table.open_last_scope(self)
                rnv = self.symbol_table.get_symbol(rnv.name, None, s)['type']
                ##rnv = self.cur_symbol_table.get_symbol(rnv.name)['type']
                ##self.cur_symbol_table.close_scope(self)
            elif rnv.type == "term" or rnv.type == "factor" or rnv.type == "call":
                # IDK what to do here
                rnv = rt
            else:
                print("error197")

            if rnv != rt:
                raise Exception(f"Semantic error: Function declared return type '{rt}' but returns type '{rnv}'.")

    def semantic_function_redef_check(self, f_name:str):
        # Eerst checken da we geen functies definieren in int main()
        flag: bool = False
        for f in self.functions:
            if f[0].name == "main":
                flag = True

        name: str = f_name
        if self.cur_symbol_table.name == [0] and name != "main" and flag:
            raise Exception(f"Error: Definition of '{name}' in local scope.")

        # daarna functies redef checken
        for i in range(0,len(self.functions)):
            if self.functions[i][0].name == f_name:
                if self.functions[i][1] == False:
                    self.functions[i] = (self.functions[i][0],True)
                else:
                    fa: list[str] = self.append_arguments(self.functions[i][0].arguments)

                    raise Exception(f"Semantic error: redefinition of the function '{f_name}' with parameters {fa}")



    def visitFunction(self, ctx: CParser.FunctionContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = FunctionNode()
        node.declaration = self.visitFunction_declaration(ctx.function_declaration())

        self.semantic_function_redef_check(node.declaration.name)

        node.block = self.visitBlock_scope(ctx.block_scope())

        self.semantic_return_check(node)

        node.children = [node.declaration, node.block]
        return node

    def visitBlock_scope(self, ctx: CParser.Block_scopeContext, loop: bool = False):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = BlockNode()
        nodes = []
        statements = ctx.statement()
        self.cur_symbol_table.open_scope(self)
        for statement in statements:
            temp = self.visitStatement(statement, loop)
            if isinstance(temp, tuple):
                for t in temp:
                    nodes.append(t)
            else:
                if temp.type == "break" or temp.type == "continue":
                    break
                nodes.append(temp)
        node.children = nodes

        self.cur_symbol_table.close_scope(self)
        return node

    def visitStatement(self, ctx: CParser.StatementContext,loop:bool = False):
        if ctx.exception is not None:
            raise Exception("syntax error")
        self.line_nr += 1

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
            node.statement = self.visitJump_statement(ctx.jump_statement(), loop)
            node.children.append(node.statement)
        elif ctx.compound_statement():
            node = self.visitCompound_statement(ctx.compound_statement(), loop)
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
        self.semantic_rede_check(node, False, True)
        return node

    def visitArray(self, ctx: CParser.ArrayContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = ArrayNode()
        node.name = ctx.IDENTIFIER().getText()
        node.index = self.visitLogicexpression(ctx.logicexpression())

        if node.index.type not in ["term","factor","call"] and node.index.literalType == "float":
            raise Exception(f"Semantic Error; Can't access array '{node.name}' with index '{node.index.value}' of type float.")
        else:
            s = self.cur_symbol_table.get_symbol(node.name)
            if s["type"][0:5] != "array":
                raise Exception(
                    f"Semantic Error; Can't access type '{s['type']}' with index '{node.index.value}'; '{node.name}' is not an array.")
        return node

    def compare_arguments(self, f_args: list[FunctionArgNode], call_args: list[ArgumentNode]) -> list[list]:
        f_args1:list = []
        call_args1:list = []
        for fa in f_args:
            f_args1.append(fa.varType)

        for ca in range(0, len(call_args)):
            if call_args[ca].value.type == "unary":
                type = self.cur_symbol_table.get_symbol(call_args[ca].value.variable.name)["type"]
                call_args1.append(type + "*")
            elif call_args[ca].value.type == "variable":
                call_args1.append(self.cur_symbol_table.get_symbol(call_args[ca].value.name)["type"])
            elif call_args[ca].value.type == "term":
                call_args1.append(f_args1[ca])

            else:

                call_args1.append(call_args[ca].value.literalType)

        return [f_args1, call_args1]

    def semantic_call_check(self, node:CallNode):
        # First check for calling noexistent function
        found = 0  # 0: not found, 1 : found but undeclared, 2 : ok
        for f in self.functions:
            if f[0].name == node.name:
                if f[1]:
                    function = f[0]
                    found = 2
                else:
                    found = max(found, 1)
        if found == 1:
            raise Exception(f"Error: Calling undefined function '{node.name}'.")
        elif found == 0:
            raise Exception(f"Error: Calling undeclared function '{node.name}'.")

        # Second check for wrong function parameters

        f_args = function.arguments
        call_args = node.arguments

        s = self.compare_arguments(f_args,call_args)
        if s[0] != s[1]:
            raise Exception(f"Function call for '{node.name}' expected parameters {s[0]}; but got {s[1]}.")


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
        if ctx.argument():
            node.arguments = self.visitArgument(ctx.argument())
            node.children = node.arguments

        self.semantic_call_check(node)

        return node

    def visitScanf(self, ctx: CParser.ScanfContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = ScanfNode()
        node.string = ctx.STRINGLITERAL().getText()[1:-1]
        if ctx.argument():
            node.arguments = self.visitArgument(ctx.argument())

        for arg in node.arguments:
            if arg.value.type == "unary":
                n = arg.value.variable.name
                self.cur_symbol_table.symbol_used_twice(n)
                #self.cur_symbol_table.add_symbol_value(n, "None", line_nr)

        return node

    def parse_string(self, string:str) -> list[str]:
        string.replace(" ", "")
        if string[-2:] == "\n":
            string = string[:-2]

        list: list = []
        for i in range(0, len(string)):
            if string[i] == "%":
                list.append(string[i:i+2])

        return list

    def semantic_printf_check(self, node:PrintfNode):
        if len(node.arguments) == 0:
            return
        s = self.parse_string(node.string)

        # Parse node.arguments
        na: list = []
        for a in node.arguments:
            if isinstance(a.value, str):
                na.append("string")
            elif a.value.type == "literal":
                na.append(a.value.literalType)
            else:
                return

        len_s = len(s)
        if len_s != len(node.arguments):
            raise Exception(f"Error: Incompatible arguments:'{na}', for Printf with '{s}'.")

        for i in range (0,len_s):
            nai = na[i]
            if s[i] == "%d":
                # argument moet int zijn
                if nai != "int":
                    raise Exception(f"Error: Incompatible arguments:{na}, for Printf with:{s} (should be int).")

            elif s[i] == "%s":
                # argument moet string zijn
                if nai != "string":
                    raise Exception(f"Error: Incompatible arguments:{na}, for Printf with:{s} (should be string).")

            elif s[i] == "%c":
                # argument moet char zijn
                if nai != "char":
                    raise Exception(f"Error: Incompatible arguments:{na}, for Printf with:{s} (should be char).")

            elif s[i] == "%f":
                # argument moet float zijn
                if nai != "float":
                    if nai == "int":
                        print((f"Warning: Incompatible arguments:{na}, for Printf with:{s} (should be float)."))
                    else:
                        raise Exception(f"Error: Incompatible arguments:{na}, for Printf with:{s} (should be float).")

            else:
                print(s[i])


    def visitPrintf(self, ctx: CParser.PrintfContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = PrintfNode()
        node.string = ctx.STRINGLITERAL().getText()[1:-1]
        node.scope = self.cur_symbol_table.name

        if ctx.argument():
            node.arguments = self.visitArgument(ctx.argument())

        self.semantic_printf_check(node)
        return node

    def visitArgument(self, ctx: CParser.ArgumentContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = ArgumentNode()
        if ctx.logicexpression():
            node.value = self.visitLogicexpression(ctx.logicexpression())
        else:
            node.value = ctx.STRINGLITERAL().getText()

        if ctx.COMMA():
            allArgs = [node]
            arguments = self.visitArgument(ctx.argument())
            for arg in arguments:
                allArgs.append(arg)
            return allArgs
        return [node]

    def visitJump_statement(self, ctx: CParser.Jump_statementContext, loop:bool = False):
        if ctx.exception is not None:
            raise Exception("syntax error")

        if ctx.break_():
            if not loop:
                raise Exception(f"Error: can't 'break' when not in loop.")
            return BreakNode()
        elif ctx.continue_():
            if not loop:
                raise Exception(f"Error: can't 'continue' when not in loop.")
            return ContinueNode()
        elif ctx.return_():
            node = ReturnNode()
            if ctx.logicexpression():
                node.returnValue = self.visitLogicexpression(ctx.logicexpression())
            else:
                node.returnValue = "void"
            node.scope = self.cur_symbol_table.name
            return node

    def visitCompound_statement(self, ctx: CParser.Compound_statementContext,  loop:bool = False):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = None
        if ctx.if_():
            node = self.visitIf(ctx.if_(), loop)
        elif ctx.while_():
            self.loop = True
            node = self.visitWhile(ctx.while_())
            self.loop = False
        elif ctx.for_():
            self.loop = True
            node = self.visitFor(ctx.for_())
            self.loop = False

        if node is None:
            raise Exception("Node is node")

        return node

    def visitIf(self, ctx: CParser.IfContext, loop:bool = False):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = IfNode()
        node.condition = self.visitCondition(ctx.condition())
        node.block = self.visitBlock_scope(ctx.block_scope(), loop)
        node.children = [node.condition, node.block]
        if ctx.else_():
            node.elseNode = self.visitElse(ctx.else_(), loop)
            node.children.append(node.elseNode)
        return node

    def visitCondition(self, ctx: CParser.ConditionContext):
        return self.visitLogicexpression(ctx.logicexpression())

    def visitElse(self, ctx: CParser.ElseContext, loop:bool = False):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = ElseNode()
        node.block = self.visitBlock_scope(ctx.block_scope(), loop)
        node.children = [node.block]
        return node

    def visitWhile(self, ctx: CParser.WhileContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        node = WhileNode()
        node.condition = self.visitCondition(ctx.condition())
        loop: bool = True
        node.block = self.visitBlock_scope(ctx.block_scope(), loop)
        node.children = [node.condition, node.block]

        return node

    # returns two nodes instead of one
    def visitFor(self, ctx: CParser.ForContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        While = WhileNode()

        Statement = StatementNode()
        condition = self.visitFor_condition(ctx.for_condition())
        Statement.statement = condition[0] # int a = 0
        Statement.children = [Statement.statement]
        While.condition = condition[1] # a >3
        loop: bool = True
        While.block = self.visitBlock_scope(ctx.block_scope(), loop)
        While.block.children.append(condition[2]) # a ++
        While.children = [While.condition, While.block]

        return Statement, While

    def visitFor_condition(self, ctx: CParser.For_conditionContext):
        if ctx.exception is not None:
            raise Exception("syntax error")

        temp = None

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
                node.left = VariableNode()
                node.left.name = ctx.getText()
                node.left.line_nr = self.line_nr
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
        else:
            node.children = []
        return node

    def visitComment(self, ctx: CParser.CommentContext):
        if ctx.exception is not None:
            raise Exception("syntax error")
        node = CommentNode()
        node.text = ctx.getText()
        #self.line_nr +=1
        return node

    def semantic_assignment_check(self, node: AssignmentNode):
        # ScanF roept dit niet op TODO
        # Adding variable values to the symbol table
        if node.right.type == 'literal':
            if node.left.type in ['instantiation', 'variable']:
                # Als de waarde van dit symbool voorheen al ingevuld is, duiden we dit aan
                # if self.symbol_table.get_symbol(node.left.name)['value'] is not None:
                if 2 == 3:
                    self.cur_symbol_table.symbol_used_twice(node.left.name)
                else:
                    n:str = node.left.name
                    if not isinstance(n,str):
                        n = n.getText()
                    self.cur_symbol_table.add_symbol_value(n, node.right.value, self.line_nr)
                    self.cur_symbol_table.symbol_used_twice(n)
                    # Scope toevoegen
                    # node.scope = self.cur_symbol_table.name

            # else:  bv. nodelefttype = unary bv "*ptr = 2;"

        # Operations of incompatible types
        # int x = 2; int b = 3; const int * x_ptr = & x; *x_ptr = b;
        if node.left.type == "unary" and node.right.type == "variable":
            nlvn = node.left.variable.name
            nlvnt = self.cur_symbol_table.get_symbol(nlvn)['type']
            if nlvnt[0:5] == "const":
                raise Exception(f"Semantic Error; Pointed value of '{nlvn}' of type '{nlvnt}' cannot be changed.")

        if node.right.type == "unary":

            if node.right.variable.type == "literal":
                nrvn = "literal"
                nrvt = node.right.variable.literalType
            elif node.right.variable.type == "variable":
                nrvn = node.right.variable.name
                nrvt = self.cur_symbol_table.get_symbol(nrvn)['type']
            elif node.right.variable.type == "unary":
                nr = node.right.variable
                while nr.type == "unary":
                    nr = nr.variable
                # Nu is nr een variabele
                nrvn = nr.name
                nrvt = self.cur_symbol_table.get_symbol(nrvn)['type']
            else:
                print("error")
                nrvt, nrvn = "error", "error"

            if node.right.operation == "*":
                if nrvt[-1] != '*':
                    raise Exception(f"Semantic Error; Can't dereference non-pointer '{nrvn}' of type '{nrvt}'.")
            elif node.right.operation == "&":
                # BV int b = 4; int** m = &b;
                nlvn = node.left.name
                if not isinstance(nlvn, str):
                    nlvn = nlvn.getText()
                nlvt = self.cur_symbol_table.get_symbol(nlvn)['type']

                if nlvt[-2:] == "**":
                    if nrvt[-1] != "*":
                        raise Exception(
                            f"Semantic Error; Can't assign address of '{nrvn}' of type '{nrvt}' to '{nlvn}' of type '{nlvt}'.")

                def trim(word: str) -> str:
                    if word[:5] == "const":
                        word = word[5:]
                    if word[-2:] == "**":
                        word = word[:-2]
                    if word[-1] == "*":
                        word = word[:-1]
                    return word

                if trim(nlvt) != trim(nrvt):
                    raise Exception(
                        f"Semantic Error; Can't assign address of '{nrvn}' of type '{nrvt}' to '{nlvn}' of Incorrect type '{nlvt}'.")

            # else: anders perfect in orde

        # Check for wrong assignment, bv: float f(); int e = f()
        if node.right.type == "call":
            nln: str = node.left.name
            if not isinstance(nln, str):
                nln = nln.getText()
            nlt:str = self.cur_symbol_table.get_symbol(nln)['type']
            for f in self.functions:
                if f[0].name == node.right.name:
                    frt = f[0].returnType #function return value type

            if nlt != frt:
                raise Exception(f"Semantic error: Operation of incompatible types; '{nlt}' get assigned to function returning :'{frt}'")

        # Assignments of incompatible types "inta=1;floatb=a;" OF "inta;floatb;a=b;"
        # bv "int a; float b; a=b;"
        if node.left.type == "variable" and node.right.type == "variable":
            nodeLn = str(node.left.name)
            nodeRn = str(node.right.name)
            nodeLt = self.cur_symbol_table.get_symbol(nodeLn)['type']
            nodeRt = self.cur_symbol_table.get_symbol(nodeRn)['type']
            if nodeLt != nodeRt:
                raise Exception(
                    f"Variable '{nodeRn}' of type '{nodeRt}' gets assigned to variable '{nodeLn}' of incompatible type '{nodeLt}'. ")

        # bv "int a = 1; float b = a;"
        if node.left.type == "instantiation" and node.right.type == "variable":
            nodeLn = str(node.left.name)
            nodeRn = str(node.right.name)
            nodeLt = str(node.left.varType)
            nodeRt = self.cur_symbol_table.get_symbol(nodeRn)['type']

            if node.left.const:
                nodeLt = "const" + nodeLt

            if nodeLt != nodeRt:
                print(
                    f"Syntax Warning; During definition, Variable '{nodeRn}' of type '{nodeRt}' gets assigned to variable '{nodeLn}' of incompatible type '{nodeLt}'. ")

    def visitAssignment(self, ctx: CParser.AssignmentContext, loop:bool = False):
        if ctx.exception is not None:
            raise Exception("syntax error")
        if ctx.rvalue_assignment():
            raise Exception(f"cannot assign rvalue {ctx.rvalue_assignment().logicexpression(0).getText()}")

        node = AssignmentNode()
        if ctx.declaration():
            node.left = self.visitDeclaration(ctx.declaration())

        # removed const instantiation

        node.right = self.visitLogicexpression(ctx.logicexpression())
        node.children = [node.left, node.right]
        node.scope = self.cur_symbol_table.name

        self.semantic_assignment_check(node)

        return node


    def semantic_undef_assign_check(self, node):
        # Use of an undefined variable
        type1 = self.cur_symbol_table.get_symbol(str(node.name), "undef")['type']

        # Assignment to a const variable.
        if type1[0:5] == "const":
            if type1[-1] == "*":
                pass
            else:
                raise Exception(
                    f"Semantic Error; Assignment to the const variable '{str(node.name)}' that has the type '{type1}'.")

    def visitDeclaration(self, ctx: CParser.DeclarationContext):
        if ctx.exception is not None:
            raise Exception("syntax error")
        node = None

        # removed instantiation
        if ctx.array():
            node = self.visitArray(ctx.array())
            self.semantic_undef_assign_check(node)

        elif ctx.IDENTIFIER():  # bv x:var = 3
            node = VariableNode()
            node.name = ctx.getText()
            self.semantic_undef_assign_check(node)

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

    def semantic_array_compare_check(self, node: CompareNode):

        if node.left.type == "variable":
            nln = node.left.name
            ls = self.cur_symbol_table.get_symbol(nln)["type"]
            lsa = ls[0:5]
        elif node.left.type == "literal":
            ls = node.left.literalType
            lsa = ls
        else:
            return

        if node.right.type == "variable":
            nrn = node.right.name
            rs = self.cur_symbol_table.get_symbol(nrn)["type"]
            rsa = rs[0:5]
        elif node.right.type == "literal":
            rs = node.right.literalType
            rsa = rs
        else:
            return


        if lsa == "array" or rsa == "array":
            raise Exception(f"Semantic error: Can't do comparison on type array; '{ls}' {node.operation} '{rs}'.")

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
            self.semantic_array_compare_check(node)
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


    # Check for incompatible types in Terms
    def semantic_types_check(self, node: TermNode):

        if node.left.type == "factor" or node.right.type == "factor":
            return
        if node.left.type == "call" or node.right.type == "call":
            return

        if node.left.type == "variable":
            nlt:str = self.cur_symbol_table.get_symbol(node.left.name)["type"]
        elif node.left.type == "unary":
            nlt = "unary"
        else:
            nlt = node.left.literalType

        if node.right.type == "variable":
            nrt:str = self.cur_symbol_table.get_symbol(node.right.name)["type"]
        elif node.right.type == "unary":
            nrt = "unary"
        else:
            if node.right.type == "term":
                return
            nrt = node.right.literalType

        if (nlt == "int" and nrt == "float") or (nlt == "float" and nrt == "int"):
            return
        if nlt != nrt or nlt[-1] == "*" or nrt[-1] == "*":
            raise Exception(f"Semantic error: Operation of incompatible types; '{nlt}' {node.operation} '{nrt}'")


    def visitTerm(self, ctx: CParser.TermContext):
        if ctx.exception is not None:
            raise Exception("syntax error")
        if not ctx.termops():
            # bv int a = 1;
            node = self.visitFactor(ctx.factor(0))
            return node
        node = TermNode()
        node.operation = ctx.termops().getText()
        node.left = self.visitFactor(ctx.factor(0))

        #a = self.cur_symbol_table.get_symbol(str(node.name), "undef")
        #if a['value'] is None:
        #    raise Exception(f"Syntax Error; Symbol '{node.name}' is uninitialized")

        if ctx.term():
            node.right = self.visitTerm(ctx.term())
        else:
            # bv ... = . + .;
            node.right = self.visitFactor(ctx.factor(1))
        node.children = [node.left, node.right]

        self.semantic_types_check(node)

        # bv int a = 1+2; =>  node.left.value = 1      node.right.value = 2
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

                raise Exception(f"Error: Dereference with '{node.operation}' has wrong mismatched type of '{node.variable.literalType}'.")
            node.children = [node.variable]

        elif ctx.literal():
            node = self.visitLiteral(ctx.literal())
        elif ctx.pointer():
            node = self.visitPointer(ctx.pointer())
        elif ctx.IDENTIFIER():
            node = VariableNode()
            node.name = ctx.IDENTIFIER().__str__()
            node.line_nr = self.line_nr
            if self.loop:
                node.line_nr = - node.line_nr
            # Use of an undeclared variable
            self.cur_symbol_table.get_symbol(str(node.name), "undef")
        elif ctx.array():
            node = self.visitArray(ctx.array())
        elif ctx.logicexpression():
            node = self.visitLogicexpression(ctx.logicexpression())
        elif ctx.function_call():
            node = self.visitFunction_call(ctx.function_call())
        if ctx.SPECIALUNARY():
            newNode = SpecialUnaryNode()
            newNode.operation = ctx.SPECIALUNARY().__str__()
            newNode.variable = node
            newNode.children = [newNode.variable]
            node = newNode
        return node

    def visitPointer(self, ctx: CParser.PointerContext):
        if ctx.exception is not None:
            raise Exception("syntax error")
        node = UnaryNode()
        node.operation = ctx.STAR().__str__()
        variable = None
        if ctx.IDENTIFIER():
            variable = VariableNode()
            variable.name = ctx.IDENTIFIER().__str__()
            variable.line_nr = self.line_nr
            # Use of an uninitialized variable
            self.cur_symbol_table.get_symbol(str(variable.name), "unint")
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
