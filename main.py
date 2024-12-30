class Lexer:
    def __init__(self, source_code_input):
        self.source_code = source_code_input
        self.position = 0
        self.tokens = []
        self._tokenize()

    def _tokenize(self):
        keywords = {"scope", "print"}

        while self.position < len(self.source_code):
            char = self.source_code[self.position]

            if char.isspace():
                self.position += 1
            elif char.isalpha():  # Identifier or keyword
                start = self.position
                while self.position < len(self.source_code) and (
                        self.source_code[self.position].isalnum() or self.source_code[self.position] == '_'):
                    self.position += 1
                word = self.source_code[start:self.position]
                if word in keywords:
                    self.tokens.append(("KEYWORD", word))
                else:
                    self.tokens.append(("IDENTIFIER", word))
            elif char.isdigit():  # Integer literal
                start = self.position
                while self.position < len(self.source_code) and self.source_code[self.position].isdigit():
                    self.position += 1
                number = self.source_code[start:self.position]
                self.tokens.append(("NUMBER", int(number)))
            elif char == '{':
                self.tokens.append(("LBRACE", char))
                self.position += 1
            elif char == '}':
                self.tokens.append(("RBRACE", char))
                self.position += 1
            elif char == '=':
                self.tokens.append(("EQUALS", char))
                self.position += 1
            else:
                raise ValueError(f"Unexpected character: {char}")

    def next_token(self):
        if self.tokens:
            return self.tokens.pop(0)
        return "EOF", None


if __name__ == '__main__':
    with open("source_code.txt") as f:
        source_code = f.read()
        lexer = Lexer(source_code)
        scopes = [dict()]
        while (token := lexer.next_token())[0] != "EOF":
            # print(token)
            if token[0] == "IDENTIFIER":
                if (lexer.next_token())[0] != "EQUALS":
                    print("Syntax Error: Expected '=' after identifier")
                id_source = lexer.next_token()
                current_scope = scopes[-1]
                id_val = id_source[1] if id_source[0] == "NUMBER" else (
                    scopes[-1][id_source[1]] if id_source[1] in scopes[-1] else 'null')
                current_scope[token[1]] = id_val
            elif token[0] == "KEYWORD":
                if token[1] == "scope":
                    if (lexer.next_token())[0] != "LBRACE":
                        print("Syntax Error: Expected '{' after scope keyword")
                    scopes.append(dict())
                elif token[1] == "print":
                    identifier = lexer.next_token()
                    if identifier[0] != "IDENTIFIER":
                        print("Syntax Error: Expected identifier after print keyword")
                    else:
                        print(scopes[-1][identifier[1]] if identifier[1] in scopes[-1] else 'null')
                else:
                    print("Syntax Error: Unexpected keyword")
            elif token[0] == "RBRACE":
                scopes.pop()
