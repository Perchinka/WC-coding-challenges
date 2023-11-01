class Lexer:
    def __init__(self):
        self.SYNTAX = ['{', '}', '[', ']', ':', ',']


    def lex(self, json_string: str):
        tokens = []

        while len(json_string):
            string, json_string = self.lex_string(json_string)
            if string is not None:
                tokens.append(string)
                continue

            number, json_string = self.lex_number(json_string)
            if number is not None:
                tokens.append(number)
                continue

            boolean, json_string = self.lex_bool(json_string)
            if boolean is not None:
                tokens.append(boolean)
                continue

            null, json_string = self.lex_null(json_string)
            if null:
                tokens.append(None)
                continue

            whitespace, json_string = self.lex_whitespace(json_string)
            if whitespace is not None:
                continue

            if json_string[0] in self.SYNTAX:
                tokens.append(json_string[0])
                json_string = json_string[1:]
                continue
            else:
                raise Exception(f'Invalid JSON string: Unexpected character {json_string[0]}')
            
        return tokens
        
    def lex_string(self, json_string: str):
        if json_string[0] != '"':
            return None, json_string

        json_string = json_string[1:]
        string = ''
        for char in json_string:
            if char == '"':
                return string, json_string[len(string) + 1:]
            else:
                string += char
        raise Exception('Expected end quote')
    
    def lex_number(self, json_string: str):
        number = ''

        allowed_chars = [str(i) for i in range(0,10)]+['-', '.', 'e']
        for char in json_string:
            if char in allowed_chars:
                number += char
            else:
                break

        if not number:
            return None, json_string
        
        if '.' in number:
            return float(number), json_string[len(number):]
        
        return int(number), json_string[len(number):]
    
    def lex_null(self, json_string: str):
        if json_string[:4] == 'null':
            return True, json_string[4:]
        return None, json_string
    
    def lex_bool(self, json_string: str):
        if json_string[:4] == 'true':
            return True, json_string[4:]
        elif json_string[:5] == 'false':
            return False, json_string[5:]
        return None, json_string
    
    def lex_whitespace(self, json_string: str):
        if json_string[0] in ' \t\n':
            return True, json_string[1:]
        return None, json_string