from name import Name


class TableExpr:
    def __init__(self, val):
        self.val = val

    @staticmethod
    def isTableExpr(tokens):
        return Name.isName(tokens)
