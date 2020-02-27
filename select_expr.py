from tokens import Tokens
from name import Name


class SelectExpr:
    def __init__(self, val):
        self.val = val

    @staticmethod
    def isSelectExpr(tokens: list):
        if len(tokens) == 1:
            if tokens[0] == Tokens.WILDCARD:
                return True
            if Name.isName(tokens[0]):
                return True
        else:
            isRight = True
            for i in range(0, len(tokens) - 1, 2):
                if not Name.isName(tokens[i]) or tokens[i + 1] != Tokens.COMMA:
                    isRight = False
                    break

            if not Name.isName(tokens[len(tokens) - 1]):
                isRight = False

            return isRight
