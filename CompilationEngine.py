"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

from JackTokenizer import JackTokenizer

SYMBOLS = ["{", "}", "[", "]", "(", ")", ".", ",", ";", "+", "-", "*", "/",
           "&", "|", "<", ">", "=", "~"]

KEYWORDS = ["class", "method", "function", "constructor", "int", "boolean",
            "char", "void", "var", "static", "field", "let", "do", "if",
            "else", "while", "return", "true", "false", "null", "this"]


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: typing.TextIO,
                 output_stream: typing.TextIO) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        self.jack_tokenizer = JackTokenizer(input_stream)
        self.stream = output_stream
        self.str_statement = ""
        pass

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # Your code goes here!
        self.str_statement += "<tokens>\n"

        self.str_statement += "<class>\n"

        self.str_statement += self.jack_tokenizer.eat("***")  # class
        self.str_statement += self.jack_tokenizer.eat("***")  # class name
        self.str_statement += self.jack_tokenizer.eat("***")  # {
        while self.jack_tokenizer.is_next_class_var_dec():
            self.compile_class_var_dec()
        while self.jack_tokenizer.is_next_class_sub_dec():
            self.compile_subroutine()
        self.str_statement += self.jack_tokenizer.eat("***")  # }
        self.str_statement += "</class>\n"
        self.str_statement += "</tokens>\n"
        self.stream.write(self.str_statement)

        pass

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        self.str_statement += "<classVarDec>\n"
        self.str_statement += self.jack_tokenizer.eat("***")  # static|field
        self.str_statement += self.jack_tokenizer.eat("***")  # type
        self.str_statement += self.jack_tokenizer.eat("***")  # varName
        check = self.jack_tokenizer.eat(",")
        while check != "":
            self.str_statement += check
            self.str_statement += self.jack_tokenizer.eat("***")  # varName
            check = self.jack_tokenizer.eat(",")
        self.str_statement += self.jack_tokenizer.eat("***")  # ;
        self.str_statement += "</classVarDec>\n"
        pass

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function, or constructor."""
        # Your code goes here!
        self.str_statement += "<subroutineDec>\n"

        self.str_statement += self.jack_tokenizer.eat("***")  # (constractor|function|method)
        self.str_statement += self.jack_tokenizer.eat("***")  # type|void
        self.str_statement += self.jack_tokenizer.eat("***")  # subroutine name
        self.str_statement += self.jack_tokenizer.eat("***")  # (
        self.compile_parameter_list()
        self.str_statement += self.jack_tokenizer.eat("***")  # )


        self.str_statement += "<subroutineBody>\n"
        self.str_statement += self.jack_tokenizer.eat("***")  # {
        while self.jack_tokenizer.is_next_var_dec():
            self.compile_var_dec()
        self.compile_statements()
        self.str_statement += self.jack_tokenizer.eat("***")  # }
        self.str_statement += "</subroutineBody>\n"
        self.str_statement += "</subroutineDec>\n"

        pass

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        self.str_statement += "<parameterList>\n"

        if not self.jack_tokenizer.is_next_is_par():
            self.str_statement += self.jack_tokenizer.eat("***")  # type
            self.str_statement += self.jack_tokenizer.eat("***")  # varName
            check = self.jack_tokenizer.eat(",")
            while check != "":
                self.str_statement += check
                self.str_statement += self.jack_tokenizer.eat("***")  # type
                self.str_statement += self.jack_tokenizer.eat("***")  # varName
                check = self.jack_tokenizer.eat(",")
        self.str_statement += "</parameterList>\n"

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
        self.str_statement += "<varDec>\n"
        self.str_statement += self.jack_tokenizer.eat("***")  # var
        self.str_statement += self.jack_tokenizer.eat("***")  # type
        self.str_statement += self.jack_tokenizer.eat("***")  # varName
        check = self.jack_tokenizer.eat(",")
        while check != "":
            self.str_statement += check
            self.str_statement += self.jack_tokenizer.eat("***")  # varName
            check = self.jack_tokenizer.eat(",")
        self.str_statement += self.jack_tokenizer.eat("***")  # ;
        self.str_statement += "</varDec>\n"

        pass

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # Your code goes here!
        self.str_statement += "<Statements>\n"
        stam = self.jack_tokenizer.is_next_statment()
        while stam != "":
            if stam == "let":
                self.compile_let()
            elif stam == "if":
                self.compile_if()
            elif stam == "while":
                self.compile_while()
            elif stam == "do":
                self.compile_do()
            else:
                self.compile_return()
            stam = self.jack_tokenizer.is_next_statment()
        self.str_statement += "</Statements>\n"

        pass

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        self.str_statement += "<doStatement>\n"
        self.str_statement += self.jack_tokenizer.eat("***")  # do
        self.str_statement += self.jack_tokenizer.eat("***")  # (className|varName)
        if self.jack_tokenizer.is_next_dot():
            self.str_statement += self.jack_tokenizer.eat("***")  # .
            self.str_statement += self.jack_tokenizer.eat("***")  # name
        self.str_statement += self.jack_tokenizer.eat("***")  # (
        self.compile_expression_list()
        self.str_statement += self.jack_tokenizer.eat("***")  # )
        self.str_statement += self.jack_tokenizer.eat("***")  # ;
        self.str_statement += "</doStatement>\n"

        pass

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        self.str_statement += "<letStatement>\n"

        self.str_statement += self.jack_tokenizer.eat("***")  # let
        self.str_statement += self.jack_tokenizer.eat("***")  # var name
        if self.jack_tokenizer.is_next_is_bracket():
            self.str_statement += self.jack_tokenizer.eat("***")  # [
            self.compile_expression()
            self.str_statement += self.jack_tokenizer.eat("***")  # ]
        self.str_statement += self.jack_tokenizer.eat("***")  # =
        self.compile_expression()
        self.str_statement += self.jack_tokenizer.eat("***")  # ;
        self.str_statement += "</letStatement>\n"

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        self.str_statement += "<whileStatement>\n"

        self.str_statement += self.jack_tokenizer.eat("***")  # while
        self.str_statement += self.jack_tokenizer.eat("***")  # (
        self.compile_expression()
        self.str_statement += self.jack_tokenizer.eat("***")  # )
        self.str_statement += self.jack_tokenizer.eat("***")  # {
        self.compile_statements()
        self.str_statement += self.jack_tokenizer.eat("***")  # }
        self.str_statement += "</whileStatement>\n"

        pass

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        self.str_statement += "<returnStatement>\n"

        self.str_statement += self.jack_tokenizer.eat("***")  # return
        if not self.jack_tokenizer.is_next_poi_br():
            self.compile_expression()
        self.str_statement += self.jack_tokenizer.eat("***")  # ;
        self.str_statement += "</returnStatement>\n"

        pass

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        self.str_statement += "<ifStatement>\n"

        self.str_statement += self.jack_tokenizer.eat("***")  # if
        self.str_statement += self.jack_tokenizer.eat("***")  # (
        self.compile_expression()
        self.str_statement += self.jack_tokenizer.eat("***")  # )
        self.str_statement += self.jack_tokenizer.eat("***")  # {
        self.compile_statements()
        self.str_statement += self.jack_tokenizer.eat("***")  # }
        check = self.jack_tokenizer.eat("else")
        if check != "":  # else
            self.str_statement += check
            self.str_statement += self.jack_tokenizer.eat("***")  # {
            self.compile_statements()
            self.str_statement += self.jack_tokenizer.eat("***")  # }
        self.str_statement += "</ifStatement>\n"

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        self.str_statement += "<expression>\n"
        self.compile_term()
        while self.jack_tokenizer.is_next_is_op():
            self.str_statement += self.jack_tokenizer.eat("***") # op
            self.compile_term()
        self.str_statement += "</expression>\n"

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        # Your code goes here!
        self.str_statement += "<term>\n"
        if self.jack_tokenizer.token_type() == "STRING_CONST" or self.jack_tokenizer.token_type() == "INT_CONST" or  self.jack_tokenizer.is_next_k_w_const():
            self.str_statement += self.jack_tokenizer.eat("***")# num or string or k_w_const
        elif self.jack_tokenizer.is_next_is_un_op():
            self.str_statement += self.jack_tokenizer.eat("***")# unary op
            self.compile_term()
        elif self.jack_tokenizer.is_next_is_par():
            self.str_statement += self.jack_tokenizer.eat("***")# (
            self.compile_expression()
            self.str_statement += self.jack_tokenizer.eat("***")# )
        else:
            self.str_statement += self.jack_tokenizer.eat("***")  # varName |className
            if self.jack_tokenizer.is_next_is_bracket():
                self.str_statement += self.jack_tokenizer.eat("***")  # [
                self.compile_expression()
                self.str_statement += self.jack_tokenizer.eat("***")  # ]
            elif self.jack_tokenizer.is_next_dot():
                self.str_statement += self.jack_tokenizer.eat("***")  # .
                self.str_statement += self.jack_tokenizer.eat("***")  # subroutone name
                self.str_statement += self.jack_tokenizer.eat("***")  # (
                self.compile_expression_list()
                self.str_statement += self.jack_tokenizer.eat("***")  # )
            elif self.jack_tokenizer.is_next_is_left_par():
                self.str_statement += self.jack_tokenizer.eat("***")  # subroutone name
                self.str_statement += self.jack_tokenizer.eat("***")  # (
                self.compile_expression_list()
                self.str_statement += self.jack_tokenizer.eat("***")  # )


        self.str_statement += "</term>\n"
        pass

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!

        self.str_statement += "<expressions>\n"
        if not self.jack_tokenizer.is_next_is_right_par():
            self.compile_expression()
            check = self.jack_tokenizer.eat(",")
            while check != "":
                self.str_statement += check
                self.compile_expression()
                check = self.jack_tokenizer.eat(",")
        self.str_statement += "</expressions>\n"

