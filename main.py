import os

from Antlr.CLexer import CLexer
from AstVisitor import *
from AST import AST
from AstOptimizer import AstOptimizer
from MIPSVisitor import *

# Test script that automatically runs our Compiler on specified C files.
# Just run "python3 main.py"


def main():
    vis_tree_flag: bool = True
    vis_st_flag: bool = False

    tests_directory_path = "tests/alle_projecten/CorrectCode"
    # tests_directory_path = "tests/abc"
    asm_directory_path = "tests/output/asm_files"

    for filename in os.listdir(tests_directory_path):
        print(f"\nEntering project {filename}. \n", flush=True)
        file_path = os.path.join(tests_directory_path, filename)

        if os.path.isfile(file_path):
            input_stream = FileStream(file_path)
            lexer = CLexer(input_stream)
            tokens = CommonTokenStream(lexer)
            parser = CParser(tokens)
            parser.removeErrorListeners()
            tree = parser.run()

            visitor = AstVisitor()
            # optimizer = AstOptimizer()
            # try:
            print("Entered successfully", flush=True)
            ast = visitor.visit(tree)
            # ast = optimizer.optimize(ast, visitor.symbol_table)

            if vis_tree_flag:
                ast.visualize(filename)
            # if vis_st_flag:
            #     visitor.symbol_table.st_print(True)

            # mips = MIPSVisitor()
            # mips.file = asm_directory_path + "/" + filename[0:-2] + ".asm"
            # ast.generateMips(mips)
            #
            # except Exception as error:
            #      print(error, flush=True)

        else:
            raise Exception(f"{file_path} not found.")


if __name__ == '__main__':
    main()
