from ply import yacc
from sqlLexer import SqlLexer
class SqlParser(object):
    def __init__(self,input):
        self.input=input
        self.build()
    tokens = SqlLexer.tokens
    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'NOT'),
        ('left', 'EQ', 'NE', 'LT', 'GT', 'LE', 'GE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        )
    
    def p_statement_list(self, p):
        """
        statement_list : statement
                       | statement_list statement
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]
            
    def p_statement(self, p):
        """
        statement : insert_statement
                  | select_statement
                  | import_statement
                  | update_statement
                  | delete_statement
        """
        p[0] = p[1]
    def p_import_statement(self, p):
        """
        import_statement : IMPORT PATH AS ID
        """
        if p[4] in SqlLexer.reserved:
            print("yes")
        p[0]=('import',p[2],p[4])


    def p_insert_statement(self, p):

        """
        insert_statement : INSERT INTO ID VALUES LPAREN expr_list RPAREN
                         | INSERT INTO ID LPAREN id_list RPAREN VALUES LPAREN expr_list RPAREN
                         | INSERT INTO ID VALUES LPAREN select_statement RPAREN
        """
        p[0] = ('insert', p[3], p[6])


    def p_delete_statement(self,p):
        """
        delete_statement : DELETE FROM ID opt_where_clause
        """
        p[0]=('delete',p[3],p[4])

    def p_update_statement(self,p):
        """
       update_statement : UPDATE ID SET assign_list opt_where_clause

        """
        p[0]=('update',p[2],p[4],p[5])

    def p_assign_list(self,p):
        """
        assign_list : assign_operation
                    | assign_list COMMA assign_operation
        """
        if len(p)==2:p[0]=(p[1])
        else: p[0]=p[1]+p[3]
    def p_assign_operation(self,p):
        """
        assign_operation : ID EQ atom

        """
        p[0] = (p[1],p[3])
    def p_select_statement(self, p):
        """
        select_statement : SELECT select_columns FROM ID opt_where_clause opt_orderby_clause
        """
        p[0] = ('select', p[2], p[4], p[5], p[6])
        
    def p_select_columns(self, p):
        """
        select_columns : TIMES
                       | id_list
        """
        p[0] = p[1]
        
    def p_opt_where_clause(self, p):
        """
        opt_where_clause : WHERE search_condition
                         |
        """
        if len(p) == 1:
            p[0] = None
        else:
            p[0] = p[2]
            
    def p_search_condition(self, p):
        """
        search_condition : search_condition OR search_condition
                         | search_condition AND search_condition
                         | NOT search_condition
                         | LPAREN search_condition RPAREN
                         | predicate
        """
        lenp = len(p)
        if lenp == 4:
            if p[1] == '(':
                p[0] = p[2]
            else:
                p[0] = (p[2], p[1], p[3])
        elif lenp == 3:
            p[0] = (p[1], p[2])
        else:
            p[0] = p[1]

    def p_predicate(self, p):
        """
        predicate : comparison_predicate
        """
        p[0] = p[1]
        
    def p_comparison_predicate(self, p):
        """
        comparison_predicate : scalar_exp EQ scalar_exp
                             | scalar_exp NE scalar_exp
                             | scalar_exp LT scalar_exp
                             | scalar_exp LE scalar_exp
                             | scalar_exp GT scalar_exp
                             | scalar_exp GE scalar_exp
        """
        p[0] = (p[2], p[1], p[3])
        
    # TODO: unify this with old expr rules
    def p_scalar_exp(self, p):
        """
        scalar_exp : scalar_exp PLUS scalar_exp
                   | scalar_exp MINUS scalar_exp
                   | scalar_exp TIMES scalar_exp
                   | scalar_exp DIVIDE scalar_exp
                   | atom
                   | LPAREN scalar_exp RPAREN
        """
        lenp = len(p)
        if lenp == 4:
            if p[1] == "(":
                p[0] = p[2]
            else:
                p[0] = (p[2], p[1], p[3])
        elif lenp == 2:
            p[0] = p[1]
        else:
            raise AssertionError()
        
    def p_atom(self, p):
        """
        atom : NUMBER
             | ID
             | STRING
        """
        p[0] = p[1]
            
    #order by
    def p_opt_orderby_clause(self, p):
        """
        opt_orderby_clause : ORDER BY ID
                           |
        """
        if len(p) == 1:
            p[0] = None
        else:
            p[0] = p[3]
            

    def p_id_list(self, p):
        """
        id_list : id_value
                | id_list COMMA id_value
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_id_value(self,p):
        """
               id_value : NUMBER
                       | ID
               """
        p[0]=p[1]

    def p_expr_list(self, p):
        """
        expr_list : expr
                  | expr_list COMMA expr
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_expr(self, p):
        """
        expr : expr PLUS term
             | expr MINUS term
             | term
             | ID
             | STRING
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ('binop', p[2], p[1], p[3])
            
    def p_term(self, p):
        """
        term : term TIMES factor
             | term DIVIDE factor
             | factor
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ('binop', p[2], p[1], p[3])

    def p_factor(self, p):
        """
        factor : NUMBER
               | LPAREN expr RPAREN
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2] 

    def p_error(self, p):
        print ("Syntax error in input") # TODO: at line %d, pos %d!" % (p.lineno)
    
    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser

    def parse(self):
        lexer = SqlLexer().build()
        if self.input:
            result = self.parser.parse(self.input, lexer=lexer)
            return result
        return None
    '''
    l.build()
    l.test()
        
def unittest_parser():
    p = SqlParser()
    p.build()
    p.test()
    
if __name__ == "__main__":    
 # unittest_lexer()
   unittest_parser()
    '''
                
