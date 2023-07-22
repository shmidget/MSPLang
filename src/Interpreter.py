import Parser
import Lexxer
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()

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
    def ThrowError(self, ErrorMessage):
        print(f"{Fore.RED}{Style.BRIGHT}Halting program as error was thrown!")
        print(f"{Fore.RED}Error {Style.RESET_ALL}: {Fore.YELLOW}" + ErrorMessage)
        print(Style.RESET_ALL)
        exit()

    def EvaluateExpression(self, expression):

        for Index, Token in enumerate(expression):
            if Token.Type == Lexxer.TOKEN_TYPE.MISC:
                try:
                    expression[Index] = self.Variables[Token.Value]
                except:
                    self.ThrowError(f"No such variable with name {Fore.WHITE}" + Token.Value)

        while len(expression) != 1:
            for Index, Token in enumerate(expression):
               
                if Token.Type == Lexxer.TOKEN_TYPE.CONCATENATION:
                    LeftSide = expression[Index - 1]
                    RightSide = expression[Index + 1]

                    if LeftSide.Type != RightSide.Type:
                        self.ThrowError("Arithmetic on mismatched types!")

                    EvaluatedValue = str(LeftSide.Value) + " " + str(RightSide.Value)

                    expression[Index] = Lexxer.Token(EvaluatedValue, Lexxer.TOKEN_TYPE.STRING)

                    expression.remove(LeftSide)
                    expression.remove(RightSide)

                elif Token.Type == Lexxer.TOKEN_TYPE.ADDITION:
                    LeftSide = expression[Index - 1]
                    RightSide = expression[Index + 1]

                    if LeftSide.Type != RightSide.Type:
                        self.ThrowError("Arithmetic on mismatched types!")

                    EvaluatedValue = LeftSide.Value + RightSide.Value

                    expression[Index] = Lexxer.Token(EvaluatedValue, LeftSide.Type)

                    expression.remove(LeftSide)
                    expression.remove(RightSide)
                if Token.Type == Lexxer.TOKEN_TYPE.SUBTRACTION:
                    LeftSide = expression[Index - 1]
                    RightSide = expression[Index + 1]

                    if LeftSide.Type != RightSide.Type:
                        self.ThrowError("Arithmetic on mismatched types!")

                    EvaluatedValue = LeftSide.Value - RightSide.Value

                    expression[Index] = Lexxer.Token(EvaluatedValue, LeftSide.Type)

                    expression.remove(LeftSide)
                    expression.remove(RightSide)
                if Token.Type == Lexxer.TOKEN_TYPE.MULTIPLICATION:
                    LeftSide = expression[Index - 1]
                    RightSide = expression[Index + 1]

                    if LeftSide.Type != RightSide.Type:
                        self.ThrowError("Arithmetic on mismatched types!")

                    EvaluatedValue = LeftSide.Value * RightSide.Value

                    expression[Index] = Lexxer.Token(EvaluatedValue, LeftSide.Type)

                    expression.remove(LeftSide)
                    expression.remove(RightSide)
                if Token.Type == Lexxer.TOKEN_TYPE.DIVISION:
                    LeftSide = expression[Index - 1]
                    RightSide = expression[Index + 1]

                    if LeftSide.Type != RightSide.Type:
                        self.ThrowError("Arithmetic on mismatched types!")

                    EvaluatedValue = LeftSide.Value / RightSide.Value

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
