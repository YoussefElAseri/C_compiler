class SymbolTable:
    def __init__(self, parent=None):
        self.scope: dict = {}  # 1 scope
        self.childScopes: list[SymbolTable] = []  # Children
        self.parentScope: SymbolTable = parent

    def openScope(self):
        newScope = SymbolTable()
        newScope.parentScope = self
        self.childScopes.append(newScope)
        return newScope

    def closeScope(self):
        if not self.parentScope:
            raise Exception("Current scope doesn't have a parent scope!")

        return self.parentScope

    def retrieveEntryCurrentScope(self, name):
        if self.scope[name]:
            return self.scope[name], True
        return None, False

    def retrieveEntry(self, name):
        currentScope: SymbolTable = self
        searchResult = currentScope.retrieveEntryCurrentScope(name)
        if searchResult[1]:
            return searchResult[0], True
        while currentScope.parentScope:
            currentScope = currentScope.parentScope
            searchResult = currentScope.retrieveEntryCurrentScope(name)
            if searchResult[1]:
                return searchResult[0], True
        return None, False

    def addVariableEntry(self, name, variableType, const=False):
        if self.retrieveEntryCurrentScope(name)[1]:
            raise Exception(f"Redeclaration: Symbol '{name}' already declared in current scope!")
        self.scope[name] = {'type': variableType, 'assignments': 0, 'uses': 0, 'const': const}

    def addFunctionEntry(self, name, definition, returnType, *args):
        function = self.retrieveEntry(name)
        if function[1]:
            identical = function[0]["return"] == returnType and function[0]["arguments"] == args
            if not identical:
                raise Exception(f"function {name} redeclared with different signature!")
            if function[0]["definition"] and definition:
                raise Exception(f"function {name} has multiple different definitions!")
            if function[0]["definition"] or definition:
                function[0]["definition"] = True
        else:
            self.scope[name] = {'type': 'function', 'return': returnType, 'arguments': args, 'definition': definition,
                                'calls': 0}

    def addArrayEntry(self, name, variableType):
        if self.retrieveEntryCurrentScope(name)[1]:
            raise Exception(f"Redeclaration: Symbol '{name}' already declared in current scope!")

        self.scope[name] = {'type': "array", "variableType": variableType}

    def addAssignment(self, name):
        variable = self.retrieveEntry(name)
        if not variable[1]:
            raise Exception(f"Variable {name} has not been declared yet!")
        if variable[0]['const']:
            raise Exception(f"Const variable reassigned!")
        variable[0]['assignments'] += 1

    def addUse(self, name):
        retrievedVariable = self.retrieveEntry(name)
        if not retrievedVariable[1]:
            raise Exception(f"Variable {name} has not been declared yet!")
        retrievedVariable[0]['uses'] += 1

    def addCall(self, name):
        function = self.retrieveEntry(name)
        if not function[1]:
            raise Exception(f"Function {name} hasn't been declared yet!")
        function[0]["calls"] += 1

    def checkEntry(self, name, entryType):
        if not self.retrieveEntry(name)[1]:
            raise Exception(f"{entryType} {name} has not been initialised yet!")



class Contexts:
    def __init__(self):
        self.loopId = 0
        self.functionContexts = []
        self.loopContexts = []

    def pushFunction(self, name):
        self.functionContexts.append(name)

    def peekFunction(self):
        if len(self.loopContexts) == 0:
            raise Exception("Return statement outside of function")
        return self.functionContexts[-1]

    def popFunction(self):
        self.functionContexts.pop()

    def pushLoop(self):
        self.functionContexts.append(self.loopId)
        self.loopId += 1

    def peekLoop(self):
        if len(self.loopContexts) == 0:
            raise Exception("Break or continue statement outside of loop")
        return self.loopContexts[-1]

    def popLoop(self):
        if len(self.loopContexts) == 0:
            raise Exception("Break or continue statement outside of loop")
        self.loopContexts.pop()
