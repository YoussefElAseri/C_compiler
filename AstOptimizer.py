import SymbolTable
from AST import AST
from Nodes import *


class AstOptimizer:
    st: SymbolTable

    def optimize(self, tree: AST, st: SymbolTable):
        return self.constantFolding(self.constantPropagation(tree, st))

    # We gaan loopen over elke expression en elke identifier vervangen met zijn waarde.
    def constantPropagation(self, tree: AST, st: SymbolTable):
        self.st = st
        propagated = True
        while propagated:
            propagated = self.constantPropagationRecursive(tree.root)
        return tree

    def constantPropagationRecursive(self, node: Node):
        propagated = False



        # First, we will fill in the variables in a printf function.
        # The printf node, will have no children
        if node.type == "printf":
            for i in range(0,len(node.arguments)):
                av = node.arguments[i].value

                if not isinstance(av,str) and av.type == "variable":
                    cln: int = av.line_nr
                    if cln < 0:
                        continue

                    avn: str = node.arguments[i].value.name
                    s: list = node.scope
                    avs = self.st.get_symbol(avn, None, s)
                    if not avs["assignOnce"]:
                        continue
                    v = self.st.get_most_recent_value(avn, cln, s)

                    #if avs['value'] is not None and avs['assignOnce'] is True:
                    if v is not None:
                        new_node = LiteralNode()
                        new_node.value = v
                        nlt = avs['type']
                        if nlt[0:5] == "const":
                            nlt = nlt[5:]
                        new_node.literalType = nlt
                        node.arguments[i].value = new_node


        # Secondly, all other nodes
        for i in range(len(node.children)):
            childNode = node.children[i]
            if childNode.type == "assignment":
                crt = childNode.right.type

                # assignment .right logicexpression/-boolexpression/-term .right factor/element
                if crt == "variable":
                    s = childNode.scope
                    #print( "s " +str(childNode) +  str(s) + str(len(s)))

                    cnrs = self.st.get_symbol(childNode.right.name, None, s)
                    if cnrs['value'] is not None and cnrs['assignOnce'] is True:
                        v = cnrs['value']
                        node = LiteralNode()
                        node.value = v
                        nlt = cnrs['type']
                        if nlt[0:5] == "const":
                            nlt = nlt[5:]
                        node.literalType = nlt
                        childNode.right = node
                        childNode.children[1] = node

                elif childNode.right.type == "term":
                    """print(childNode.right.type)
                    print( childNode.right.right.type)
                    print( childNode.right.left.type)
                    print()"""

                    # Checken of er een identifier links en/of rechts is
                    # Als de variabele meerdere keren geassigned wordt doen we niets
                    if childNode.right.left.type == "variable":
                        symbol0 = self.st.get_symbol(childNode.right.left.name, None, childNode.scope)
                        if symbol0['value'] is not None and symbol0['assignOnce'] is True:
                            # identifier vervangen met waarde

                            # 1 waarde opzoeken in symbol table
                            v = symbol0['value']

                            # 2 nieuwe literal node aanmaken
                            node = LiteralNode()
                            node.value = v
                            nlt = symbol0['type']
                            if nlt[0:5] == "const":
                                nlt = nlt[5:]
                            node.literalType = nlt
                            # 3 variable node in Term node, vervangen met literal node
                            childNode.right.left = node
                            childNode.right.children[0] = node

                    if childNode.right.right.type == "variable":
                        symbol0 = self.st.get_symbol(childNode.right.right.name, "unint",childNode.scope)
                        if symbol0['value'] is not None and symbol0['assignOnce'] is True:
                            v = symbol0['value']
                            node = LiteralNode()
                            node.value = v
                            nlt = symbol0['type']
                            if nlt[0:5] == "const":
                                nlt = nlt[5:]
                            node.literalType = nlt
                            childNode.right.right = node
                            childNode.right.children[1] = node

        self.delReturnStatement(node)

        for child in node.children:

            if self.constantPropagationRecursive(child):
                propagated = True
        return propagated

    def delReturnStatement(self, node:BlockNode):
        # Do not generate code for statements that appear after a return in a function
        rbc = ["return", "break", "continue"]
        for c2 in range(0, len(node.children)):
            ncc2c = node.children[c2].children
            if ncc2c and ncc2c[0].type in rbc:
                # Statements na 'return' verwijderen
                # 1 uit blockNode.children ( general Node attribute )
                node.children = node.children[0:c2 + 1]

                # 2 uit blockNode.nodes ( Block node specific attribute )
                if (node.block is not None):
                    print("error")
                break

    def constantFolding(self, tree: AST):
        folded = True
        while folded:
            folded = self.constantFoldingRecursive(tree.root)
        return tree

    def constantFoldingRecursive(self, node: Node):
        folded = False
        for i in range(len(node.children)):
            childNode = node.children[i]
            if (childNode.type == "logic" or childNode.type == "compare" or childNode.type == "term"
                    or childNode.type == "factor" or childNode.type == "unary" or childNode.type == "special_unary"):
                result = childNode.foldConstant()
                if result is not None:
                    node.children[i] = result

                    # node has to be an operation node
                    if node.type == "unary" or node.type == "special_unary":
                        node.variable = result
                    elif i == 1:
                        node.right = result
                    else:
                        node.left = result
                    folded = True
        for child in node.children:
            if self.constantFoldingRecursive(child):
                folded = True
        return folded
