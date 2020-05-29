from tokenizer.token_list_builder import TokensTypes as tt
import re


class ExpressionTreeBuilder:
    @staticmethod
    def buildExprTree(tokenList: list, index: int):
        andCondition, index = ExpressionTreeBuilder.andCondition(tokenList, index)

        if andCondition is None:
            return None, None

        if len(tokenList) == index or tokenList[index][0] != tt.OR:
            return Expression(andCondition), index

        if tokenList[index][0] == tt.OR:
            expression, index = ExpressionTreeBuilder.buildExprTree(tokenList, index + 1)
            return Expression(andCondition=andCondition, expression=expression), index
        else:
            return None, None

    @staticmethod
    def andCondition(tokenList: list, index: int):
        # lastPosition - индекс токена с которого надо продолжать
        condition, index = ExpressionTreeBuilder.condition(tokenList, index)

        if condition is None:
            return None, None

        if len(tokenList) == index or tokenList[index][0] != tt.AND:
            return AndCondition(condition), index

        if tokenList[index][0] == tt.AND:
            and_condition, index = ExpressionTreeBuilder.andCondition(tokenList, index + 1)
            return AndCondition(condition=condition, andCondition=and_condition), index
        else:
            return None, None

    @staticmethod
    def condition(tokenList: list, index: int):
        isNot = False
        expression = None
        firstOperand = None
        compare = None
        secondOperand = None
        isLike = False

        if tokenList[index][0] == tt.NOT:
            isNot = True
            expression, index = ExpressionTreeBuilder.buildExprTree(tokenList, index + 1)
        elif tokenList[index][0] == tt.OPEN_BRACKET:
            nextIndex = index + 1
            countBrackets = 1
            while countBrackets > 0:
                if tokenList[nextIndex][0] == tt.OPEN_BRACKET:
                    countBrackets += 1
                elif tokenList[nextIndex][0] == tt.CLOSE_BRACKET:
                    countBrackets -= 1

                nextIndex += 1

            expression, index = ExpressionTreeBuilder.buildExprTree(tokenList[index + 1:nextIndex - 1], 0)

            index = nextIndex
        else:
            firstOperand, index = ExpressionTreeBuilder.summand(tokenList, index)
            if firstOperand is None:
                return None, None

            if len(tokenList) == index:
                return Condition(operandFirst=firstOperand), index

            compareTokens = [tt.LESS, tt.LESS_OR_EQUAL, tt.EQUAL, tt.MORE, tt.MORE_OR_EQUAL, tt.NOT_EQUAL]
            if tokenList[index][0] == tt.NOT:
                isNot = True

                index += 1
                if len(tokenList) == index:
                    return None, None

                if tokenList[index][0] == tt.LIKE:
                    isLike = True
                    secondOperand, index = ExpressionTreeBuilder.summand(tokenList, index + 1)
                else:
                    return None, None
            elif tokenList[index][0] == tt.LIKE:
                isLike = True
                secondOperand, index = ExpressionTreeBuilder.summand(tokenList, index + 1)
            elif tokenList[index][0] in compareTokens:
                compare, index = ExpressionTreeBuilder.compare(tokenList, index)
                if len(tokenList) == index or compare is None:
                    return None, None

                secondOperand, index = ExpressionTreeBuilder.summand(tokenList, index)
                if secondOperand is None:
                    return None, None
            else:
                return Condition(operandFirst=firstOperand), index

        return Condition(operandFirst=firstOperand, expression=expression, isNot=isNot,
                         compare=compare, operandSecond=secondOperand, like=isLike), index

    @staticmethod
    def compare(tokenList: list, index: int):
        compareList = [tt.MORE, tt.LESS, tt.NOT_EQUAL, tt.LESS_OR_EQUAL, tt.MORE_OR_EQUAL, tt.EQUAL]
        if tokenList[index][0] in compareList:
            return Compare(tokenList[index]), index + 1
        else:
            return None, None

    @staticmethod
    def summand(tokenList: list, index: int):
        factor, index = ExpressionTreeBuilder.factor(tokenList, index)
        operation = None

        if factor is None:
            return None, None

        if len(tokenList) == index:
            return Summand(factor=factor), index

        operationList = [tt.MINUS, tt.PLUS]
        if tokenList[index][0] in operationList:
            operation = tokenList[index][0]
        else:
            return Summand(factor=factor), index

        index += 1
        if len(tokenList) == index:
            return None, None

        summand, index = ExpressionTreeBuilder.summand(tokenList, index)
        return Summand(factor, operation, summand), index

    @staticmethod
    def factor(tokenList: list, index: int):
        term, index = ExpressionTreeBuilder.term(tokenList, index)
        operation = None

        if term is None:
            return None, None

        if len(tokenList) == index:
            return Factor(term=term), index

        operationList = [tt.DIVIDE, tt.MULTIPLY]
        if tokenList[index][0] in operationList:
            operation = tokenList[index][0]
        else:
            return Factor(term=term), index

        index += 1
        if len(tokenList) == index:
            return None, None

        factor, index = ExpressionTreeBuilder.factor(tokenList, index)
        return Factor(term, operation, factor), index

    @staticmethod
    def term(tokenList: list, index: int):
        allowedTokenTypes = [tt.DIGIT, tt.NAME, tt.NULL]

        if tokenList[index][0] not in allowedTokenTypes:
            return None, None

        return Term(tokenList[index]), index + 1


class Expression:
    def __init__(self, andCondition, expression=None):
        self.andCondition = andCondition
        self.expression = expression


class AndCondition:
    def __init__(self, condition, andCondition=None):
        self.condition = condition
        self.andCondition = andCondition


class Condition:
    def __init__(self, operandFirst=None, expression=None, isNot=False, compare=None, operandSecond=None, like=False):
        self.operandFirst = operandFirst
        self.expression = expression
        self.isNot = isNot
        self.compare = compare
        self.operandSecond = operandSecond
        self.like = like


class Summand:
    def __init__(self, factor, operator=None, summand=None):
        self.factor = factor
        self.operator = operator
        self.summand = summand


class Factor:
    def __init__(self, term, operator=None, factor=None):
        self.term = term
        self.operator = operator
        self.factor = factor


class Term:
    def __init__(self, value):
        self.value = value


class Compare:
    def __init__(self, operation):
        self.operation = operation
