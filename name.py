from tokens import Tokens
import re


class Name:
    def __init__(self, val):
        self.val = val

    @staticmethod
    def isName(tokens: list) -> bool:
        if len(tokens) != 1:
            return False
        else:
            return bool(
                re.fullmatch(
                    r'(`\S+`|[A-Za-z_][A-Za-z_0-9]*(\.[A-Za-z_0-9]+)?)',
                    tokens[0]
                )
            )

