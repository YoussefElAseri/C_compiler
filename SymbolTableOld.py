class AstVisitor:
    pass


class SymbolTable:
    def __init__(self, name: list[int]):
        """
        self.subscopes; De scopes die in 'deze' scope zitten.
        """
        self.scope: dict = {}  # 1 scope
        self.subScopes: list[SymbolTable] = []  # Children
        self.parentScope: SymbolTable = None
        self.name: list[int] = name

    def add_symbol(self, name, type, function:bool = False, register = None):
        # Function=True -> function parameter
        if name in self.scope and not function:
            if self.get_symbol(name)['type'] == type:
                # self.st_print()
                raise Exception(f"Redeclaration: Symbol '{name}' already declared in current scope")
            else:
                raise Exception(f"Redefinition: Symbol '{name}' already defined in current scope")
        else:
            if object:
                self.scope[name] = {'type': type, 'value': None, 'assignOnce': True, 'declarations': [], 'reg': register}
            else:
                self.scope[name] = {'type': type, 'value': None, 'assignOnce': True, 'declarations': []}

    def symbol_used_current(self, name: str):
        if name not in self.scope:
            return False
        elif self.scope[name]['value'] is None:
            return False
        else:
            return True

    def symbol_used_twice(self, name: str):
        """
        This function gets called when a symbol has a declaration.
        The symbol then gets marked with 'assignOnce'.
        This is relevant for Constant Propagation.
        :param name: The symbol
        :return:
        """
        self.scope[name]['assignOnce'] = False

    def add_symbol_value(self, name, value, line_nr:int = -99):
        if line_nr == -99:
            raise Exception("input line nr")

        if name not in self.scope:
            # Als je in een diepere functie bent, wordt dit symbool ineens toegevoegd aan de huidige scope
            symbol = self.get_symbol(name, "undef")
            # instantieren in huidige scope
            self.add_symbol(name, symbol['type'])

        self.scope[name]['value'] = value
        # line_nr ook toevoegen
        self.scope[name]['declarations'].append([line_nr, value])

    def get_symbol(self, name, errortype=None, input_scope: list[int] = None):
        scope = self
        if input_scope is not None and len(input_scope) > 0:
            input_scope = input_scope.copy()
            input_scope.pop(0)
            for s in input_scope:
                if s > len(scope.subScopes):
                    print("errorSy")
                scope = scope.subScopes[s]

        while scope is not None:
            if name in scope.scope:
                return scope.scope[name]
            scope = scope.parentScope

        if errortype == "undef":
            raise Exception(f"Syntax Error; Symbol '{name}' is undefined")
        elif errortype == "unint":
            raise Exception(f"Syntax Error; Symbol '{name}' is uninitialized")
        else:
            print(f"\nGet Symbol Error: {name} , {input_scope} , {errortype}, {self.scope} ")
            print(f"{self.parentScope.scope}")
            scope.st_print()
            raise Exception(f"Symbol '{name}' is ?????????")

    def get_most_recent_value(self, name:str, cln: int, cs: list) -> int:
        # cln = current line number
        value:int = 0
        vln: int = 0  # var_st_line_nr: lijn van de declaratie van deze waarde
        flag: bool = False

        scopes = cs.copy()
        scopes.pop(0)
        scope = self
        while scope is not None:

            symbol = {}
            if name in scope.scope.keys():
                symbol = scope.scope[name]
            else:
                symbol['declarations'] = []

            for decl in symbol['declarations']:
                vln = decl[0]
                if vln < cln:
                    flag = True
                    value = decl[1]
                elif vln == cln:
                    print("error97")
            if scopes:
                scope = scope.subScopes[scopes[0]]
                scopes.pop(0)
            else:
                scope = None

        if flag:
            return value
        else:
            return None

    def open_scope(self, vis: AstVisitor):
        new_name = self.name.copy()
        new_id = 0 + len(self.subScopes)
        new_name.append(new_id)
        new_st = SymbolTable(new_name)
        new_st.parentScope = self

        self.subScopes.append(new_st)
        vis.cur_symbol_table = new_st

    def close_scope(self, vis: AstVisitor):
        # self.st_print()
        # self.scopes.pop(-1)
        # self.curScope =- 1
        vis.cur_symbol_table = self.parentScope

    def open_last_scope(self, vis: AstVisitor):

        vis.cur_symbol_table = self.subScopes[-1]


    def st_print(self, flag=True):  # flag=True voor de main plaats waar je st_print oproept
        n = self
        if flag:
            print("*****")

        print(f"Scope {self.name}:")

        if len(self.scope) == 0:
            print("empty")
        else:
            for name, info in self.scope.items():
                print(f"{name} => {info}")

        print()
        ""
        for x in n.subScopes:
            print("Subscope: ")
            x.st_print(False)
        if flag:
            print("*___*")

        """for i in range(0,len(self.scopes)):
            print(f"Scope {i}:")
            for name, info in self.scopes[i].items():
                print(f"{name} => {info}")
            print()"""
