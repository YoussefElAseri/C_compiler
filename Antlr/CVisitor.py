# Generated from Antlr/C.g4 by ANTLR 4.12.0
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

# This class defines a complete generic visitor for a parse tree produced by CParser.

class CVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CParser#run.
    def visitRun(self, ctx:CParser.RunContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#include.
    def visitInclude(self, ctx:CParser.IncludeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#global_var.
    def visitGlobal_var(self, ctx:CParser.Global_varContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#function.
    def visitFunction(self, ctx:CParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#forward_declare.
    def visitForward_declare(self, ctx:CParser.Forward_declareContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#function_declaration.
    def visitFunction_declaration(self, ctx:CParser.Function_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#argument_declaration.
    def visitArgument_declaration(self, ctx:CParser.Argument_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#function_call.
    def visitFunction_call(self, ctx:CParser.Function_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#printf.
    def visitPrintf(self, ctx:CParser.PrintfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#scanf.
    def visitScanf(self, ctx:CParser.ScanfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#argument.
    def visitArgument(self, ctx:CParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#statement.
    def visitStatement(self, ctx:CParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#array_initialisation.
    def visitArray_initialisation(self, ctx:CParser.Array_initialisationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#block_scope.
    def visitBlock_scope(self, ctx:CParser.Block_scopeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#compound_statement.
    def visitCompound_statement(self, ctx:CParser.Compound_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#expression_statement.
    def visitExpression_statement(self, ctx:CParser.Expression_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#jump_statement.
    def visitJump_statement(self, ctx:CParser.Jump_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#if.
    def visitIf(self, ctx:CParser.IfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#else.
    def visitElse(self, ctx:CParser.ElseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#while.
    def visitWhile(self, ctx:CParser.WhileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#for.
    def visitFor(self, ctx:CParser.ForContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#break.
    def visitBreak(self, ctx:CParser.BreakContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#continue.
    def visitContinue(self, ctx:CParser.ContinueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#return.
    def visitReturn(self, ctx:CParser.ReturnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#condition.
    def visitCondition(self, ctx:CParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#for_condition.
    def visitFor_condition(self, ctx:CParser.For_conditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#update_expression.
    def visitUpdate_expression(self, ctx:CParser.Update_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#comment.
    def visitComment(self, ctx:CParser.CommentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#assignment.
    def visitAssignment(self, ctx:CParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#rvalue_assignment.
    def visitRvalue_assignment(self, ctx:CParser.Rvalue_assignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#declaration.
    def visitDeclaration(self, ctx:CParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#instantiationExpression.
    def visitInstantiationExpression(self, ctx:CParser.InstantiationExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#not_const.
    def visitNot_const(self, ctx:CParser.Not_constContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#const.
    def visitConst(self, ctx:CParser.ConstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#type.
    def visitType(self, ctx:CParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#logicexpression.
    def visitLogicexpression(self, ctx:CParser.LogicexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#boolexpression.
    def visitBoolexpression(self, ctx:CParser.BoolexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#term.
    def visitTerm(self, ctx:CParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#factor.
    def visitFactor(self, ctx:CParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#element.
    def visitElement(self, ctx:CParser.ElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#array.
    def visitArray(self, ctx:CParser.ArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#logicops.
    def visitLogicops(self, ctx:CParser.LogicopsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#compops.
    def visitCompops(self, ctx:CParser.CompopsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#termops.
    def visitTermops(self, ctx:CParser.TermopsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#factorops.
    def visitFactorops(self, ctx:CParser.FactoropsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#unaryops.
    def visitUnaryops(self, ctx:CParser.UnaryopsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#typecast.
    def visitTypecast(self, ctx:CParser.TypecastContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#pointer.
    def visitPointer(self, ctx:CParser.PointerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#literal.
    def visitLiteral(self, ctx:CParser.LiteralContext):
        return self.visitChildren(ctx)



del CParser