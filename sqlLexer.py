from ply import lex

class SqlLexer(object):
    reserved = {
        'import': 'IMPORT',
        'insert': 'INSERT',
        'into': 'INTO',
        'select': 'SELECT',
        'update': 'UPDATE',
          'set': 'SET',
        'delete': 'DELETE',
        'from': 'FROM',
        'where': 'WHERE',
        'order': 'ORDER',
        'by': 'BY',
        'values': 'VALUES',
        'and': 'AND',
        'or': 'OR',
        'not': 'NOT',
        'as': 'AS',
    }

    tokens = ['NUMBER',
              'ID',
              'PATH',
              'STRING',
              'COMMA', 'SEMI',
              'PLUS', 'MINUS',
              'TIMES', 'DIVIDE',
              'LPAREN', 'RPAREN',
              'GT', 'GE',
              'LT', 'LE',
              'EQ', 'NE',
              ] + list(reserved.values())

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_PATH(self, t):
        r'[a-zA-Z]:*[a-zA-Z_0-9\\]*\.csv'
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = SqlLexer.reserved.get(t.value, 'ID')
        t.value = t.value.lower()
        #t.type = SqlLexer.reserved.get(t.value, 'ID')
        return t

    def t_STRING(self, t):
        '(?:"(?:[^"\\n\\r\\\\]|(?:"")|(?:\\\\x[0-9a-fA-F]+)|(?:\\\\.))*")|(?:\'(?:[^\'\\n\\r\\\\]|(?:\'\')|(?:\\\\x[0-9a-fA-F]+)|(?:\\\\.))*\')'
        t.value = eval(t.value)

        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_ignore = ' \t'

    literals = ['+', '-', '*', '/', '>', '>', '<', '<', '=', '=']
    # Regular expression
    t_COMMA = r'\,'
    t_SEMI = r';'
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_GT = r'>'
    t_GE = r'>='
    t_LT = r'<'
    t_LE = r'<='
    t_EQ = r'='
    t_NE = r'!='



    def t_error(self, t):
        raise TypeError("Unknown text '%s'" % (t.value,))

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer

    def test(self):
        while True:
            text = input("sql> ").strip()
            if text.lower() == "quit":
                break
            self.lexer.input(text)
            while True:
                tok = self.lexer.token()
                if not tok:
                    break
                print(tok)

#l=SqlLexer()
#l.build()
#l.test()