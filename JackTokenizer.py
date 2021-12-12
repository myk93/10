"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


KEYWORDS = ["class", "method", "function", "constructor", "int", "boolean",
             "char", "void", "var", "static", "field", "let", "do", "if",
             "else", "while", "return", "true", "false", "null", "this"]

SYMBOLS = ["{", "}", "[", "]", "(", ")", ".", ",", ";", "+", "-", "*", "/",
            "&", "|", "<", ">", "=", "~"]


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    """

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        # Your code goes here!
        # A good place to start is:
        self.tokenized_lines = []
        self.input_lines = input_stream.read().splitlines()
        self.cleanup_lines()
        self.tokenize_lines()
        self.current = -1

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        if self.current >= len(self.tokenized_lines):
            return false
        return true


    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token. 
        This method should be called if has_more_tokens() is true. 
        Initially there is no current token.
        """
        self.current += 1

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        # Your code goes here!
        if self.tokenized_lines[self.current] in KEYWORDS:
            return "KEYWORD"
        if self.tokenized_lines[self.current] in SYMBOLS:
            return "SYMBOL"
        if str(self.tokenized_lines[self.current][0]).isdigit():
            return "INT_CONST"
        if self.tokenized_lines[self.current][0] == '"':
            return "STRING_CONST"
        else:
            return "IDENTIFIER"

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", 
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO", 
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        return str(self.tokenized_lines[self.current]).upper()

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
        """
        return self.tokenized_lines[self.current]

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
        """
        # Your code goes here!
        return self.tokenized_lines[self.current]

    def int_val(self) -> int:
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
        """
        return int(self.tokenized_lines[self.current])

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double 
            quotes. Should be called only when token_type() is "STRING_CONST".
        """
        return self.tokenized_lines[self.current]

    def cleanup_lines(self) -> None:
        """Removes all comments from the input stream.
        """
        i = 0
        while i != len(self.input_lines):
            # remove empty lines and inline comments
            if len(self.input_lines[i].replace(" ", "")) == 0 or self.input_lines[i].replace(" ", "")[0] == "/":
                self.input_lines.pop(i)
            # remove lines between /* and */
            elif self.input_lines[i].replace(" ", "")[0:2] == "/*":
                while self.input_lines[i].replace(" ", "")[0:2] != "*/":
                    self.input_lines.pop(i)
                self.input_lines.pop(i)
            else:
                ' '.join(self.input_lines[i].split())
                i += 1

    def tokenize_lines(self):
        """Tokenizes the input stream.
        """
        self.tokenized_lines = []
        # split the line from input_lines where there is a space and '(', ')', '{', '}', '.', ',' , ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~', '"'
        for i in range(len(self.input_lines)):
            for spChar in SYMBOLS:
                self.input_lines[i] = self.input_lines[i].replace(spChar, " "+spChar+" ")
            str(self.input_lines[i].replace("'", ""))
            " ".join(self.input_lines[i].split())
        for i in range(len(self.input_lines)):
            self.tokenized_lines.append(self.input_lines[i].split())
        self.tokenized_lines = [s for S in self.tokenized_lines for s in S]









