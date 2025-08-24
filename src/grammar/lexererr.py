class LexerError(Exception):
    def __str__(self):
        return self.message


class ErrorToken(LexerError):
    def __init__(self, s):
        self.message = "Error Token " + s
