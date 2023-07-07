from Nodes import *
from graphviz import Digraph
import networkx as nx
import networkx.drawing.nx_pydot as nxd
import pydot
import matplotlib.pyplot as plt
import graphviz
import sys

class AST:
    root = None
    symbol_table = None
    declarations = None

    # Define the visualize function
    def vis(self, fn: str):
        node = self.root
        # Create a new Digraph object
        dot = graphviz.Digraph()

        # Define a recursive function to visit each node in the AST
        def visit(node, parent=None):
            skip_flag = False
            # Assign a unique ID to the node gebaseerd op zijn memory address
            id = str(hash(node) % ((sys.maxsize + 1) * 2))
            # Label the node with its class name
            if isinstance(node, str):
                label = node
            else:
                label = node.getASTvalue()

            if label == "'\x00'":
                label = "/0"
            elif label == "compare":
                label = node.operation
            elif label == "assignment":
                label = "="
            elif label == "line" or label == "special_unary": # Geen 'line' nodes in AST
                skip_flag = True
                id = parent

            if not skip_flag:
                dot.node(id, label)

            # Add an edge from the parent node to this node
            if parent and not skip_flag:
                dot.edge(parent, id)

            if label == "printf":
                for arg in node.arguments:
                    visit(arg.value, id)

            if not isinstance(node,str):
                # Recursively visit each child node
                for child in node.children:
                    # Node child is another AST node, visit it
                    visit(child, id)

        # Call the visit function to traverse the entire AST
        visit(node)

        # Return the DOT code as a string
        # return dot.source
        dotfilename = f'tests/output/ast_files/dot_files/{fn}.dot'

        with open(dotfilename, 'w') as f:
            f.write(dot.source)
        # Converteer the Dot file to a graphViz graph with Pydot
        (graph,) = pydot.graph_from_dot_file(dotfilename)
        graph.write_png(f'tests/output/ast_files/{fn}.png')

    def generateLLVM(self, llvm):
        self.root.generateCode(llvm)

    def generateMips(self, mips):
        self.root.generateMips(mips)
