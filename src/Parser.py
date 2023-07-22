import Lexxer

class NodeType():
    VARIABLE_NODE = 0
    PRINT_NODE = 1
    CONDITIONAL_NODE = 2
    INCREMENT_SCOPE = 3
    DECREMENT_SCOPE = 4

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
    
class ConditionalNode():
    def __init__(self, NodeType, Expression) -> None:
        self.NodeType = NodeType

        self.Expression = Expression
    def __repr__(self) -> str:
        return "(NODE: {} {})".format("CONDITION", self.Expression)

class IncrementScope():
    def __init__(self, NodeType) -> None:
        self.NodeType = NodeType
    def __repr__(self) -> str:
        return "(NODE: {})".format("INCREMENT-SCOPE")

class DecrementScope():
    def __init__(self, NodeType) -> None:
        self.NodeType = NodeType
    def __repr__(self) -> str:
        return "(NODE: {})".format("DECREMENT-SCOPE")

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

        if self.CurrentToken.Type != Lexxer.TOKEN_TYPE.LPAREN:
            print("Missing LBracket.")
            return
        
        self.AdvanceToken()
        
        Expression = []

        while self.CurrentToken.Type != Lexxer.TOKEN_TYPE.RPAREN:
            Expression.append(self.CurrentToken)
            self.AdvanceToken()

        self.ast.append(PrintNode(NodeType.PRINT_NODE, Expression))

    def ConditionalRule(self):
        
        if self.CurrentToken.Type != Lexxer.TOKEN_TYPE.CONDITIONAL:
            return
        
        self.AdvanceToken()

        if self.CurrentToken.Type != Lexxer.TOKEN_TYPE.LPAREN:
            print("Missing LBracket.")
            return
        
        self.AdvanceToken()
        
        Expression = []

        while self.CurrentToken.Type != Lexxer.TOKEN_TYPE.RPAREN:
            Expression.append(self.CurrentToken)
            self.AdvanceToken()

        self.ast.append(ConditionalNode(NodeType.CONDITIONAL_NODE, Expression))

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
        
    def ScopeRule(self):
        if self.CurrentToken.Type != Lexxer.TOKEN_TYPE.LBRACE and self.CurrentToken.Type != Lexxer.TOKEN_TYPE.RBRACE:
            return
        
        if self.CurrentToken.Type == Lexxer.TOKEN_TYPE.LBRACE:
            print("done")
            self.ast.append(IncrementScope(NodeType.INCREMENT_SCOPE))
            self.AdvanceToken()
        if self.CurrentToken.Type == Lexxer.TOKEN_TYPE.RBRACE:
            self.ast.append(DecrementScope(NodeType.DECREMENT_SCOPE))
            self.AdvanceToken()
        self.AdvanceToken()


    def GenerateAST(self):
        self.AdvanceToken()

        self.ast = []

        while self.CurrentTokenIndex < len(self.Tokens):
            
            # Rules #
            self.PrintRule()
            self.AssignmentRule()
            self.ConditionalRule()
            self.ScopeRule()
            self.AdvanceToken()

    
        print("Now displaying all Nodes:")
        for Node in self.ast:
            print(Node)
        print("Finished displaying all Nodes")

        return self.ast
        

def Parse(Tokens):
    return Parser(Tokens).GenerateAST()