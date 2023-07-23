
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
    RBRACE = "BRACE"
    NEW_LINE = "NL"
    DOT = "DOT"
    CONCATENATION = "CONCAT"

SYNTAX = {
    "print": TOKEN_TYPE.PRINT,
    "let": TOKEN_TYPE.VARIABLE
}

CHARACTERS = {
    "=": TOKEN_TYPE.ASSIGNMENT,
    ";": TOKEN_TYPE.NEW_LINE,
    "(": TOKEN_TYPE.LBRACE,
    ")": TOKEN_TYPE.RBRACE,
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
                print(self.CurrentCharacter)
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
                    
            print("Starting Newline")
            self.CheckExtraCharacters()
            self.ExtraCharacters = ""
            self.AdvanceLine()
            self.AdvanceCharacter()

        print("Now displaying all generated tokens:")
        for Tokens in self.GeneratedTokens:
            print(Tokens)
        print("Finished displaying all tokens")
        return self.GeneratedTokens


def Tokenize(FileContent):
    return Lexxer(FileContent).LexicalAnalysis()
