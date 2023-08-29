import pydot
import graphviz
import sys
from Nodes import *


class AST:
    root = None
    symbolTable = None
    declarations = None

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

    def generateLLVM(self, llvm):
        self.root.generateCode(llvm)

    def generateMips(self, mips):
        self.root.generateMips(mips)
