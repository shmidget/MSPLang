import Parser
import Lexxer

class Interpreter():
    def __init__(self, Nodes) -> None:
        self.Nodes = Nodes
        self.CurrentNodeIndex = -1
        self.CurrentNode = None
        self.Variables = {}
    def AdvanceNode(self):
        self.CurrentNodeIndex += 1
        if self.CurrentNodeIndex < len(self.Nodes):
            self.CurrentNode = self.Nodes[self.CurrentNodeIndex]

    def EvaluateExpression(self, expression):
        

        for Index, Token in enumerate(expression):
            if Token.Type == Lexxer.TOKEN_TYPE.MISC:
                expression[Index] = self.Variables[Token.Value]

        for Index, Token in enumerate(expression):
            if Token.Type == Lexxer.TOKEN_TYPE.ADDITION:
                LeftSide = expression[Index - 1]
                RightSide = expression[Index + 1]

                if LeftSide.Type != RightSide.Type:
                    print("Arithmetic on Mismatched types!")

                EvaluatedValue = LeftSide.Value + RightSide.Value

                expression[Index] = Lexxer.Token(EvaluatedValue, LeftSide.Type)

                expression.remove(LeftSide)
                expression.remove(RightSide)

        
        return expression[0]
    
    def HandleAssignment(self):
        
        if self.CurrentNode.NodeType != Parser.NodeType.VARIABLE_NODE:
            return
        
        VariableName = self.CurrentNode.Name
        EvaluatedExpression = self.EvaluateExpression(self.CurrentNode.Expression)
        
        self.Variables[VariableName] = EvaluatedExpression


    def HandlePrintStatement(self):
        if self.CurrentNode.NodeType != Parser.NodeType.PRINT_NODE:
            return
        
        EvaluatedExpression = self.EvaluateExpression(self.CurrentNode.Expression)

        print(EvaluatedExpression.Value)


    def Evaluate(self):
        
        self.AdvanceNode()

        while self.CurrentNodeIndex < len(self.Nodes):
            
            self.HandleAssignment()
            self.HandlePrintStatement()

            self.AdvanceNode()
        
        print("\nVariable Store:")
        print(self.Variables)
