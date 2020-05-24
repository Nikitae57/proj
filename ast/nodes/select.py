class SELECT:
    def __init__(
            self,
            selectExpressionsList,
            fromExpr,
            whereExpr=None,
            groupBy=None,
            having=None,
            orderBy=None,
            limit=None,
            isDistinct=False,
            isAll=False
    ):
        self.isAll = isAll
        self.isDistinct = isDistinct
        self.selectExpressionsList = selectExpressionsList
        self.fromExpr = fromExpr
        self.whereExpr = whereExpr
        self.groupBy = groupBy
        self.having = having
        self.orderBy = orderBy
        self.limit = limit
