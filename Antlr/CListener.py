# Generated from Antlr/C.g4 by ANTLR 4.12.0
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

# This class defines a complete listener for a parse tree produced by CParser.
class CListener(ParseTreeListener):

    # Enter a parse tree produced by CParser#run.
    def enterRun(self, ctx:CParser.RunContext):
        pass

    # Exit a parse tree produced by CParser#run.
    def exitRun(self, ctx:CParser.RunContext):
        pass


    # Enter a parse tree produced by CParser#include.
    def enterInclude(self, ctx:CParser.IncludeContext):
        pass

    # Exit a parse tree produced by CParser#include.
    def exitInclude(self, ctx:CParser.IncludeContext):
        pass


    # Enter a parse tree produced by CParser#global_var.
    def enterGlobal_var(self, ctx:CParser.Global_varContext):
        pass

    # Exit a parse tree produced by CParser#global_var.
    def exitGlobal_var(self, ctx:CParser.Global_varContext):
        pass


    # Enter a parse tree produced by CParser#function.
    def enterFunction(self, ctx:CParser.FunctionContext):
        pass

    # Exit a parse tree produced by CParser#function.
    def exitFunction(self, ctx:CParser.FunctionContext):
        pass


    # Enter a parse tree produced by CParser#forward_declare.
    def enterForward_declare(self, ctx:CParser.Forward_declareContext):
        pass

    # Exit a parse tree produced by CParser#forward_declare.
    def exitForward_declare(self, ctx:CParser.Forward_declareContext):
        pass


    # Enter a parse tree produced by CParser#function_declaration.
    def enterFunction_declaration(self, ctx:CParser.Function_declarationContext):
        pass

    # Exit a parse tree produced by CParser#function_declaration.
    def exitFunction_declaration(self, ctx:CParser.Function_declarationContext):
        pass


    # Enter a parse tree produced by CParser#argument_declaration.
    def enterArgument_declaration(self, ctx:CParser.Argument_declarationContext):
        pass

    # Exit a parse tree produced by CParser#argument_declaration.
    def exitArgument_declaration(self, ctx:CParser.Argument_declarationContext):
        pass


    # Enter a parse tree produced by CParser#function_call.
    def enterFunction_call(self, ctx:CParser.Function_callContext):
        pass

    # Exit a parse tree produced by CParser#function_call.
    def exitFunction_call(self, ctx:CParser.Function_callContext):
        pass


    # Enter a parse tree produced by CParser#printf.
    def enterPrintf(self, ctx:CParser.PrintfContext):
        pass

    # Exit a parse tree produced by CParser#printf.
    def exitPrintf(self, ctx:CParser.PrintfContext):
        pass


    # Enter a parse tree produced by CParser#scanf.
    def enterScanf(self, ctx:CParser.ScanfContext):
        pass

    # Exit a parse tree produced by CParser#scanf.
    def exitScanf(self, ctx:CParser.ScanfContext):
        pass


    # Enter a parse tree produced by CParser#argument.
    def enterArgument(self, ctx:CParser.ArgumentContext):
        pass

    # Exit a parse tree produced by CParser#argument.
    def exitArgument(self, ctx:CParser.ArgumentContext):
        pass


    # Enter a parse tree produced by CParser#statement.
    def enterStatement(self, ctx:CParser.StatementContext):
        pass

    # Exit a parse tree produced by CParser#statement.
    def exitStatement(self, ctx:CParser.StatementContext):
        pass


    # Enter a parse tree produced by CParser#array_initialisation.
    def enterArray_initialisation(self, ctx:CParser.Array_initialisationContext):
        pass

    # Exit a parse tree produced by CParser#array_initialisation.
    def exitArray_initialisation(self, ctx:CParser.Array_initialisationContext):
        pass


    # Enter a parse tree produced by CParser#block_scope.
    def enterBlock_scope(self, ctx:CParser.Block_scopeContext):
        pass

    # Exit a parse tree produced by CParser#block_scope.
    def exitBlock_scope(self, ctx:CParser.Block_scopeContext):
        pass


    # Enter a parse tree produced by CParser#compound_statement.
    def enterCompound_statement(self, ctx:CParser.Compound_statementContext):
        pass

    # Exit a parse tree produced by CParser#compound_statement.
    def exitCompound_statement(self, ctx:CParser.Compound_statementContext):
        pass


    # Enter a parse tree produced by CParser#expression_statement.
    def enterExpression_statement(self, ctx:CParser.Expression_statementContext):
        pass

    # Exit a parse tree produced by CParser#expression_statement.
    def exitExpression_statement(self, ctx:CParser.Expression_statementContext):
        pass


    # Enter a parse tree produced by CParser#jump_statement.
    def enterJump_statement(self, ctx:CParser.Jump_statementContext):
        pass

    # Exit a parse tree produced by CParser#jump_statement.
    def exitJump_statement(self, ctx:CParser.Jump_statementContext):
        pass


    # Enter a parse tree produced by CParser#if.
    def enterIf(self, ctx:CParser.IfContext):
        pass

    # Exit a parse tree produced by CParser#if.
    def exitIf(self, ctx:CParser.IfContext):
        pass


    # Enter a parse tree produced by CParser#else.
    def enterElse(self, ctx:CParser.ElseContext):
        pass

    # Exit a parse tree produced by CParser#else.
    def exitElse(self, ctx:CParser.ElseContext):
        pass


    # Enter a parse tree produced by CParser#while.
    def enterWhile(self, ctx:CParser.WhileContext):
        pass

    # Exit a parse tree produced by CParser#while.
    def exitWhile(self, ctx:CParser.WhileContext):
        pass


    # Enter a parse tree produced by CParser#for.
    def enterFor(self, ctx:CParser.ForContext):
        pass

    # Exit a parse tree produced by CParser#for.
    def exitFor(self, ctx:CParser.ForContext):
        pass


    # Enter a parse tree produced by CParser#break.
    def enterBreak(self, ctx:CParser.BreakContext):
        pass

    # Exit a parse tree produced by CParser#break.
    def exitBreak(self, ctx:CParser.BreakContext):
        pass


    # Enter a parse tree produced by CParser#continue.
    def enterContinue(self, ctx:CParser.ContinueContext):
        pass

    # Exit a parse tree produced by CParser#continue.
    def exitContinue(self, ctx:CParser.ContinueContext):
        pass


    # Enter a parse tree produced by CParser#return.
    def enterReturn(self, ctx:CParser.ReturnContext):
        pass

    # Exit a parse tree produced by CParser#return.
    def exitReturn(self, ctx:CParser.ReturnContext):
        pass


    # Enter a parse tree produced by CParser#condition.
    def enterCondition(self, ctx:CParser.ConditionContext):
        pass

    # Exit a parse tree produced by CParser#condition.
    def exitCondition(self, ctx:CParser.ConditionContext):
        pass


    # Enter a parse tree produced by CParser#for_condition.
    def enterFor_condition(self, ctx:CParser.For_conditionContext):
        pass

    # Exit a parse tree produced by CParser#for_condition.
    def exitFor_condition(self, ctx:CParser.For_conditionContext):
        pass


    # Enter a parse tree produced by CParser#update_expression.
    def enterUpdate_expression(self, ctx:CParser.Update_expressionContext):
        pass

    # Exit a parse tree produced by CParser#update_expression.
    def exitUpdate_expression(self, ctx:CParser.Update_expressionContext):
        pass


    # Enter a parse tree produced by CParser#comment.
    def enterComment(self, ctx:CParser.CommentContext):
        pass

    # Exit a parse tree produced by CParser#comment.
    def exitComment(self, ctx:CParser.CommentContext):
        pass


    # Enter a parse tree produced by CParser#assignment.
    def enterAssignment(self, ctx:CParser.AssignmentContext):
        pass

    # Exit a parse tree produced by CParser#assignment.
    def exitAssignment(self, ctx:CParser.AssignmentContext):
        pass


    # Enter a parse tree produced by CParser#rvalue_assignment.
    def enterRvalue_assignment(self, ctx:CParser.Rvalue_assignmentContext):
        pass

    # Exit a parse tree produced by CParser#rvalue_assignment.
    def exitRvalue_assignment(self, ctx:CParser.Rvalue_assignmentContext):
        pass


    # Enter a parse tree produced by CParser#declaration.
    def enterDeclaration(self, ctx:CParser.DeclarationContext):
        pass

    # Exit a parse tree produced by CParser#declaration.
    def exitDeclaration(self, ctx:CParser.DeclarationContext):
        pass


    # Enter a parse tree produced by CParser#instantiationExpression.
    def enterInstantiationExpression(self, ctx:CParser.InstantiationExpressionContext):
        pass

    # Exit a parse tree produced by CParser#instantiationExpression.
    def exitInstantiationExpression(self, ctx:CParser.InstantiationExpressionContext):
        pass


    # Enter a parse tree produced by CParser#not_const.
    def enterNot_const(self, ctx:CParser.Not_constContext):
        pass

    # Exit a parse tree produced by CParser#not_const.
    def exitNot_const(self, ctx:CParser.Not_constContext):
        pass


    # Enter a parse tree produced by CParser#const.
    def enterConst(self, ctx:CParser.ConstContext):
        pass

    # Exit a parse tree produced by CParser#const.
    def exitConst(self, ctx:CParser.ConstContext):
        pass


    # Enter a parse tree produced by CParser#type.
    def enterType(self, ctx:CParser.TypeContext):
        pass

    # Exit a parse tree produced by CParser#type.
    def exitType(self, ctx:CParser.TypeContext):
        pass


    # Enter a parse tree produced by CParser#logicexpression.
    def enterLogicexpression(self, ctx:CParser.LogicexpressionContext):
        pass

    # Exit a parse tree produced by CParser#logicexpression.
    def exitLogicexpression(self, ctx:CParser.LogicexpressionContext):
        pass


    # Enter a parse tree produced by CParser#boolexpression.
    def enterBoolexpression(self, ctx:CParser.BoolexpressionContext):
        pass

    # Exit a parse tree produced by CParser#boolexpression.
    def exitBoolexpression(self, ctx:CParser.BoolexpressionContext):
        pass


    # Enter a parse tree produced by CParser#term.
    def enterTerm(self, ctx:CParser.TermContext):
        pass

    # Exit a parse tree produced by CParser#term.
    def exitTerm(self, ctx:CParser.TermContext):
        pass


    # Enter a parse tree produced by CParser#factor.
    def enterFactor(self, ctx:CParser.FactorContext):
        pass

    # Exit a parse tree produced by CParser#factor.
    def exitFactor(self, ctx:CParser.FactorContext):
        pass


    # Enter a parse tree produced by CParser#element.
    def enterElement(self, ctx:CParser.ElementContext):
        pass

    # Exit a parse tree produced by CParser#element.
    def exitElement(self, ctx:CParser.ElementContext):
        pass


    # Enter a parse tree produced by CParser#array.
    def enterArray(self, ctx:CParser.ArrayContext):
        pass

    # Exit a parse tree produced by CParser#array.
    def exitArray(self, ctx:CParser.ArrayContext):
        pass


    # Enter a parse tree produced by CParser#logicops.
    def enterLogicops(self, ctx:CParser.LogicopsContext):
        pass

    # Exit a parse tree produced by CParser#logicops.
    def exitLogicops(self, ctx:CParser.LogicopsContext):
        pass


    # Enter a parse tree produced by CParser#compops.
    def enterCompops(self, ctx:CParser.CompopsContext):
        pass

    # Exit a parse tree produced by CParser#compops.
    def exitCompops(self, ctx:CParser.CompopsContext):
        pass


    # Enter a parse tree produced by CParser#termops.
    def enterTermops(self, ctx:CParser.TermopsContext):
        pass

    # Exit a parse tree produced by CParser#termops.
    def exitTermops(self, ctx:CParser.TermopsContext):
        pass


    # Enter a parse tree produced by CParser#factorops.
    def enterFactorops(self, ctx:CParser.FactoropsContext):
        pass

    # Exit a parse tree produced by CParser#factorops.
    def exitFactorops(self, ctx:CParser.FactoropsContext):
        pass


    # Enter a parse tree produced by CParser#unaryops.
    def enterUnaryops(self, ctx:CParser.UnaryopsContext):
        pass

    # Exit a parse tree produced by CParser#unaryops.
    def exitUnaryops(self, ctx:CParser.UnaryopsContext):
        pass


    # Enter a parse tree produced by CParser#typecast.
    def enterTypecast(self, ctx:CParser.TypecastContext):
        pass

    # Exit a parse tree produced by CParser#typecast.
    def exitTypecast(self, ctx:CParser.TypecastContext):
        pass


    # Enter a parse tree produced by CParser#pointer.
    def enterPointer(self, ctx:CParser.PointerContext):
        pass

    # Exit a parse tree produced by CParser#pointer.
    def exitPointer(self, ctx:CParser.PointerContext):
        pass


    # Enter a parse tree produced by CParser#literal.
    def enterLiteral(self, ctx:CParser.LiteralContext):
        pass

    # Exit a parse tree produced by CParser#literal.
    def exitLiteral(self, ctx:CParser.LiteralContext):
        pass



del CParser