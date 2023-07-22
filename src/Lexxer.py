
DIGITS = list("1234567890.")

class TOKEN_TYPE():
    STRING = "STR"
    NUMBER = "NUM"
    PRINT = "LOG"
    ASSIGNMENT = "EQU"
    VARIABLE = "VAR"
    ADDITION = "ADD"
    SUBTRACTION = "SUB"
    DIVISION =  "DIV"
    MULTIPLICATION = "MUL"
    MISC = "MISC"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    NEW_LINE = "NL"
    DOT = "DOT"
    CONCATENATION = "CONCAT"
    CONDITIONAL = "IF"
    COMPARISON = "COMPARE"
    BOOLEAN = "BOOL"

SYNTAX = {
    "print": TOKEN_TYPE.PRINT,
    "if": TOKEN_TYPE.CONDITIONAL,
    "let": TOKEN_TYPE.VARIABLE,
}

CHARACTERS = {
    "=": TOKEN_TYPE.ASSIGNMENT,
    ";": TOKEN_TYPE.NEW_LINE,
    "(": TOKEN_TYPE.LPAREN,
    ")": TOKEN_TYPE.RPAREN,
    "{": TOKEN_TYPE.LBRACE,
    "}": TOKEN_TYPE.RBRACE,
    ",": TOKEN_TYPE.CONCATENATION,
    

    "+": TOKEN_TYPE.ADDITION,
    "-": TOKEN_TYPE.SUBTRACTION,
    "/": TOKEN_TYPE.DIVISION,
    "*": TOKEN_TYPE.MULTIPLICATION,
}

class Token():
    def __init__(self, Value, Type) -> None:
        self.Value = Value
        self.Type = Type
    def __repr__(self) -> str:
        return "(TOKEN: {}, {})".format(self.Type, self.Value)


class Lexxer():
    def __init__(self, FileContent) -> None:
        self.FileContent = FileContent
        self.CurrentCharacterIndex = -1
        self.CurrentLineIndex = -1
        self.CurrentLine = ""
        self.CurrentCharacter = ""

    def AdvanceCharacter(self):
        self.CurrentCharacterIndex += 1
        if self.CurrentCharacterIndex < len(self.CurrentLine):
            self.CurrentCharacter = self.CurrentLine[self.CurrentCharacterIndex]

    def AdvanceLine(self):
        self.CurrentLineIndex += 1
        if self.CurrentLineIndex < len(self.FileContent):
            self.CurrentCharacterIndex = -1
            self.CurrentLine = self.FileContent[self.CurrentLineIndex]

    def CheckExtraCharacters(self):
        if self.ExtraCharacters == "": return 
        if self.ExtraCharacters in SYNTAX:
            self.GeneratedTokens.append(Token(self.ExtraCharacters, SYNTAX[self.ExtraCharacters]))
            self.ExtraCharacters = ""
        else:
            self.GeneratedTokens.append(Token(self.ExtraCharacters, TOKEN_TYPE.MISC))
            self.ExtraCharacters = ""

    def ProduceString(self):
        String = ""
        self.AdvanceCharacter()

        while self.CurrentCharacter != "\"" and self.CurrentCharacterIndex < len(self.CurrentLine):
            String += self.CurrentCharacter
            self.AdvanceCharacter()

        self.AdvanceCharacter()
        self.GeneratedTokens.append(Token(String, TOKEN_TYPE.STRING))

    def ProduceNumber(self):
        Number = ""

        while self.CurrentCharacter in DIGITS and self.CurrentCharacterIndex < len(self.CurrentLine):
            Number += self.CurrentCharacter
            self.AdvanceCharacter()

        if Number == ".":
            self.GeneratedTokens.append(Token(".", TOKEN_TYPE.DOT))
            return

        if Number.count(".") > 1:
            self.GeneratedTokens.append(Token(Number, TOKEN_TYPE.MISC))
            return
        elif Number.count(".") == 1:
            self.GeneratedTokens.append(Token(float(Number), TOKEN_TYPE.MISC))
            return
        else:
            self.GeneratedTokens.append(Token(Number, TOKEN_TYPE.NUMBER))

    def LexicalAnalysis(self):
        self.AdvanceLine()
        self.AdvanceCharacter()

        print(self.CurrentLine)

        self.GeneratedTokens = []
        self.ExtraCharacters = ""

        while self.CurrentLineIndex < len(self.FileContent):
            while self.CurrentCharacterIndex < len(self.CurrentLine):
                if self.CurrentCharacter == " ": self.AdvanceCharacter()

                elif self.CurrentCharacter in CHARACTERS: 
                    self.CheckExtraCharacters()
                    self.GeneratedTokens.append(Token(self.CurrentCharacter, CHARACTERS[self.CurrentCharacter]))
                    self.AdvanceCharacter()

                elif self.CurrentCharacter == "\"":
                    self.CheckExtraCharacters()
                    self.ProduceString()
                elif self.CurrentCharacter in DIGITS:
                    self.CheckExtraCharacters()
                    self.ProduceNumber()

                else: 
                    self.ExtraCharacters += self.CurrentCharacter

                    if self.ExtraCharacters in SYNTAX:
                        self.GeneratedTokens.append(Token(self.ExtraCharacters, SYNTAX[self.ExtraCharacters]))
                        self.ExtraCharacters = ""

                    self.AdvanceCharacter()
                    
            self.CheckExtraCharacters()
            self.ExtraCharacters = ""
            self.GeneratedTokens.append(Token("", TOKEN_TYPE.NEW_LINE))
            self.AdvanceLine()

        for Index,Tokens in enumerate(self.GeneratedTokens):
            if Tokens.Type == TOKEN_TYPE.ASSIGNMENT and self.GeneratedTokens[Index+1].Type == TOKEN_TYPE.ASSIGNMENT:
                self.GeneratedTokens[Index] = Token("==", TOKEN_TYPE.COMPARISON)
                self.GeneratedTokens.remove(self.GeneratedTokens[Index + 1])

        print("Now displaying all generated tokens:")
        for Tokens in self.GeneratedTokens:
            print(Tokens)
        print("Finished displaying all tokens")
        return self.GeneratedTokens


def Tokenize(FileContent):
    return Lexxer(FileContent).LexicalAnalysis()
