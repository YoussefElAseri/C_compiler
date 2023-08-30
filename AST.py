import pydot
import graphviz
import sys
from Nodes import *
from SymbolTable import SymbolTable


class AST:
    root: Node = None
    symbolTable: SymbolTable = None

    def visualize(self, filename):
        dot = graphviz.Digraph()

        def visit(node: Node, parent=None):
            nodeID = str(hash(node) % ((sys.maxsize + 1) * 2))

            if not isinstance(node, ArgumentNode):
                dot.node(nodeID, repr(node))
                if parent is not None:
                    dot.edge(parent, nodeID)
            else:
                nodeID = parent

            for child in node.children:
                if not isinstance(child, str):
                    visit(child, nodeID)

        visit(self.root)

        # Return the DOT code as a string
        # return dot.source
        dotFileName = f'tests/output/ast_files/dot_files/{filename}.dot'
        with open(dotFileName, 'w') as dotFile:
            dotFile.write(dot.source)

        # Convert the Dot file to a graphViz graph with Pydot
        (graph,) = pydot.graph_from_dot_file(dotFileName)
        graph.write_png(f'tests/output/ast_files/{filename}.png')

    # remove all unused variables and functions (Na constant propagation)
    # bij de cleanup blijven de variables wel in de symbolTable (zou geen probleem mogen zijn?)

    def checkOperationsValidity(self):
        self.root.checkOperationsValidity(self.symbolTable)

    def constantFolding(self):
        self.root.constantFolding()

    def unusedCleanUp(self):
        self.root.unusedCleanup(self.symbolTable)

    def generateLLVM(self, llvm):
        self.root.generateLlvm(llvm)

    def generateMips(self, mips):
        self.root.generateMips(mips)
