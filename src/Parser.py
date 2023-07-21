import Lexxer

class NodeType():
    VARIABLE_NODE = 0
    PRINT_NODE = 1

class PrintNode():
    def __init__(self, NodeType, Expression) -> None:
        self.NodeType = NodeType

        self.Expression = Expression
    def __repr__(self) -> str:
        return "(NODE: {}, {})".format("PRINT", self.Expression)
    
class VariableNode():
    def __init__(self, NodeType, Name, Expression) -> None:
        self.NodeType = NodeType

        self.Name = Name
        self.Expression = Expression
    def __repr__(self) -> str:
        return "(NODE: {}, {} {})".format("VARIABLE", self.Name, self.Expression)


class Parser():
    def __init__(self, Tokens) -> None:
        self.Tokens = Tokens
        self.CurrentTokenIndex = -1
        self.CurrentToken = None

    def AdvanceToken(self):
        self.CurrentTokenIndex += 1
        if self.CurrentTokenIndex < len(self.Tokens):
            self.CurrentToken = self.Tokens[self.CurrentTokenIndex]


    def PrintRule(self):
        
        if self.CurrentToken.Type != Lexxer.TOKEN_TYPE.PRINT:
            return
        
        self.AdvanceToken()

        if self.CurrentToken.Type != Lexxer.TOKEN_TYPE.LBRACE:
            print("Missing LBracket.")
            return
        
        self.AdvanceToken()
        
        Expression = []

        while self.CurrentToken.Type != Lexxer.TOKEN_TYPE.RBRACE:
            Expression.append(self.CurrentToken)
            self.AdvanceToken()

        self.ast.append(PrintNode(NodeType.PRINT_NODE, Expression))

    def AssignmentRule(self):
        if self.CurrentToken.Type != Lexxer.TOKEN_TYPE.VARIABLE:
            return

        self.AdvanceToken()

        if self.CurrentToken.Type != Lexxer.TOKEN_TYPE.MISC:
            print("Expected Variable Name!")
            return
        
        VariableName = self.CurrentToken.Value

        self.AdvanceToken()

        if self.CurrentToken.Type != Lexxer.TOKEN_TYPE.ASSIGNMENT:
            print("Expected Equals Sign!")
            return
        
        self.AdvanceToken()

        Expression = []

        while self.CurrentToken.Type != Lexxer.TOKEN_TYPE.NEW_LINE:
            Expression.append(self.CurrentToken)
            self.AdvanceToken()

        self.ast.append(VariableNode(NodeType.VARIABLE_NODE, VariableName, Expression))
        

    def GenerateAST(self):
        self.AdvanceToken()

        self.ast = []

        while self.CurrentTokenIndex < len(self.Tokens):
            
            # Rules #

            self.PrintRule()
            self.AssignmentRule()

            self.AdvanceToken()

    
        print("Now displaying all tokens:")
        for Node in self.ast:
            print(Node)
        print("Finished displaying all tokens")

        return self.ast
        

def Parse(Tokens):
    return Parser(Tokens).GenerateAST()