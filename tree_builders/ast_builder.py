from ast.nodes.select import SELECT
from ast.nodes.order import ORDER
from ast.nodes.limit import LIMIT
from tokenizer.token_list_builder import TokensTypes as tt
from expression.select_expression import SelectExpression
from expression.table_expression import TableExpression
from tree_builders.expression_tree_builder import ExpressionTreeBuilder


class AstBuilder:
    @staticmethod
    def buildAst(tokenList: list):
        if tokenList[0][0] != tt.SELECT:
            return None

        result = SELECT()

        index = 1

        if tokenList[index][0] == tt.DISTINCT:
            result.isDistinct = True
            index += 1
        elif tokenList[index][0] == tt.ALL:
            result.isAll = True
            index += 1

        selectNode, index = AstBuilder.buildSelectNode(tokenList, index)
        result.selectExpressionsList = selectNode

        if index is None:
            raise Exception("Некорректно задан блок select!")

        fromNode, index = AstBuilder.buildFromNode(tokenList, index)
        result.fromExpr = fromNode

        if index is None:
            raise Exception("Некорректно задан блок from!")

        if len(tokenList) == index:
            return result


        countCheck = 0
        tempIndex = -1
        while len(tokenList) != index and countCheck < 5:
            if countCheck == 0:
                whereNode, tempIndex = AstBuilder.buildWhereNode(tokenList, index)
                if whereNode is not None:
                    result.whereExpr = whereNode
                    index = tempIndex

            elif countCheck == 1:
                groupByNode, tempIndex = AstBuilder.buildGroupByNode(tokenList, index)
                if groupByNode is not None:
                    result.groupBy = groupByNode
                    index = tempIndex

            elif countCheck == 2:
                if result.groupBy is not None:
                    havingNode, tempIndex = AstBuilder.buildHavingNode(tokenList, index)

                    if havingNode is not None:
                        result.having = havingNode
                        index = tempIndex

            elif countCheck == 3:
                orderBy, tempIndex = AstBuilder.buildOrderByNode(tokenList, index)

                if orderBy is not None:
                    result.orderBy = orderBy
                    index = tempIndex

            elif countCheck == 4:
                limitNode, tempIndex = AstBuilder.buildLimitNode(tokenList, index)

                if limitNode is not None:
                    result.limit = limitNode
                    index = tempIndex

            countCheck += 1

        if len(tokenList) == index:
            return result
        else:
            raise Exception("Некорретное выражение!")

    @staticmethod
    def buildSelectNode(tokenList: list, index: int):
        currentToken = tokenList[index]
        termsList = []
        while currentToken[0] != tt.FROM:
            if len(tokenList) == index:
                return None, None

            if currentToken[0] != tt.COMMA:
                termsList.append(currentToken)

            index += 1

            currentToken = tokenList[index]

        if len(termsList) == 0:
            return None, None
        else:
            return SelectExpression(termsList), index

    @staticmethod
    def buildFromNode(tokenList: list, index: int):
        if tokenList[index][0] != tt.FROM:
            return None, None

        index += 1

        if len(tokenList) == index:
            return None, None

        if tokenList[index][0] != tt.NAME:
            return None, None
        else:
            return TableExpression(tokenList[index]), index + 1

    @staticmethod
    def buildWhereNode(tokenList: list, index: int):
        if tokenList[index][0] != tt.WHERE:
            return None, None

        index += 1

        if len(tokenList) == index:
            return None, None

        return ExpressionTreeBuilder.buildExprTree(tokenList, index)

    @staticmethod
    def buildGroupByNode(tokenList: list, index: int):
        try:
            if tokenList[index][0] != tt.GROUP and tokenList[index + 1][0] != tt.BY:
                return None, None

            index += 2

            if len(tokenList) == index:
                return None, None

            return ExpressionTreeBuilder.buildExprTree(tokenList, index)

        except Exception:
            return None, None

    @staticmethod
    def buildHavingNode(tokenList: list, index: int):
        if tokenList[index][0] != tt.HAVING:
            return None, None

        index += 1

        if len(tokenList) == index:
            return None, None

        return ExpressionTreeBuilder.buildExprTree(tokenList, index)

    @staticmethod
    def buildOrderByNode(tokenList: list, index: int):
        try:
            if tokenList[index][0] != tt.ORDER and tokenList[index + 1][0] != tt.BY:
                return None, None

            index += 2

            if len(tokenList) == index:
                return None, None

            expression, index = ExpressionTreeBuilder.buildExprTree(tokenList, index)

            if len(tokenList) == index or expression is None:
                return None, None

            if tokenList[index][0] == tt.ASC or tokenList[index][0] == tt.DESC:
                return ORDER(expression, tokenList[index]), index + 1
            else:
                return None, None

        except Exception:
            return None, None

    @staticmethod
    def buildLimitNode(tokenList: list, index: int):
        if tokenList[index][0] != tt.LIMIT:
            return None, None

        index += 1

        if len(tokenList) == index or tokenList[index][0] != tt.DIGIT:
            return None, None
        else:
            return LIMIT(tokenList[index]), index + 1