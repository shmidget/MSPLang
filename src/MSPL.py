import Lexxer as MSPL_Lexxer
import Parser as MSPL_Parser
import Interpreter as MSPL_Interpreter

TestCase = "FeatureTesting"

print("\nTokenizer: Start\n")
Tokens = MSPL_Lexxer.Tokenize([line.strip() for line in open("tests/{}.mspl".format(TestCase), 'r')])
print("\nTokenizer: End\n")

print("\nParser: Start\n")
Abstract_Syntax_Tree = MSPL_Parser.Parse(Tokens)
print("\nParser: End\n")

print("\nInterpreter: Start\n")
MSPL_Interpreter.Interpreter(Abstract_Syntax_Tree).Evaluate()
print("\nInterpreter: End\n")