from ast.nodes.select import SELECT
from tokenizer.token_list_builder import TokensTypes as tt
from expression.select_expression import SelectExpression
from expression.table_expression import TableExpression
from tree_builders.expression_tree_builder import ExpressionTreeBuilder


class AstBuilder:
    @staticmethod
    def buildAst(tokenList: list):
        if tokenList[0][0] != tt.SELECT:
            return None

        isDistictOrAll = None
        if tokenList[1][0] == tt.DISTINCT or tokenList[1][0] == tt.ALL:
            isDistictOrAll = tokenList[1][1]

        selectNode, index = AstBuilder.buildSelectNode(tokenList, 1 if isDistictOrAll is None else 2)
        fromNode, index = AstBuilder.buildFromNode(tokenList, index)

        if len(tokenList) == index:
            if isDistictOrAll == tt.ALL:
                return SELECT(isAll=True, selectExpressionsList=selectNode, fromExpr=fromNode)
            elif isDistictOrAll == tt.DISTINCT:
                return SELECT(isDistinct=True, selectExpressionsList=selectNode, fromExpr=fromNode)
            else:
                return SELECT(selectExpressionsList=selectNode, fromExpr=fromNode)

        whereNode, index = AstBuilder.buildWhereNode(tokenList, index)

        return None

    @staticmethod
    def buildSelectNode(tokenList: list, index: int):
        currentToken = tokenList[index]
        termsList = []
        while currentToken[0] != tt.FROM:
            if len(tokenList) == index:
                return None

            if currentToken[0] != tt.COMMA:
                termsList.append(currentToken)

            index += 1

            currentToken = tokenList[index]

        if len(termsList) == 0:
            return None
        else:
            return SelectExpression(termsList), index

    @staticmethod
    def buildFromNode(tokenList: list, index: int):
        if tokenList[index][0] != tt.FROM:
            return None

        index += 1

        if len(tokenList) == index:
            return None

        if tokenList[index][0] != tt.NAME:
            return None
        else:
            return TableExpression(tokenList[index]), index + 1

    @staticmethod
    def buildWhereNode(tokenList: list, index: int):
        if tokenList[index][0] != tt.WHERE:
            return None

        index += 1

        if len(tokenList) == index:
            return None

        return ExpressionTreeBuilder.buildExprTree(tokenList, index)